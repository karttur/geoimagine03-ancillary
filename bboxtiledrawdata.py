'''
Created on 23 Mar 2021

@author: thomasgumbricht
'''

from sys import exit
import os

from geoimagine.gis import kt_gis as ktgis

from geoimagine.zipper import UnZip


def CsvFileGetPath1(listfilepath):
          
    with open(listfilepath) as f:
        
        content = f.readlines()

    tileList = [x.strip() for x in content] 
    
    tileList = [os.path.split(z)[1] for z in tileList]
    
    return tileList

def BBoxTiledRawData(volume,params):
    '''
    '''
        
    getlist = params.getlist
    
    pattern = params.pattern
    
    srcpath = params.srcpath
    
    dstpath = params.dstpath
        
    srcFP = os.path.join('/Volumes',volume,srcpath)
    
    dstFP = os.path.join('/Volumes',volume,dstpath)
    
    print ('srcFP', srcFP)
    
    print ('dstFP', dstFP)
    

    if not os.path.exists(dstFP):
        
        os.makedirs(dstFP)
        
    dstFPN = os.path.join(dstFP,'tiles.shp')
        
    print ('getlist',getlist)
    
    # Create the dst file
    
    srcFPN = os.path.join(srcFP,getlist)
    
    if os.path.isfile(srcFPN):

        tileList = CsvFileGetPath1(srcFPN)
        
        iniTile = True
    
        for tileFN in tileList:
            
            tileFPN = os.path.join(srcFP,tileFN)
            
            print (tileFPN)
            
            spatialRef, srcLayer = ktgis.GetRasterMetaData(tileFPN)
            
            ul = (srcLayer.bounds[0],srcLayer.bounds[3])
            
            ur = (srcLayer.bounds[2],srcLayer.bounds[3])
            
            lr = (srcLayer.bounds[2],srcLayer.bounds[1])
            
            ll = (srcLayer.bounds[0],srcLayer.bounds[1])
            
            if iniTile:
                
                fieldDefD = {'type':'string','transfer':'constant','source':tileFN,'width':8}

                fieldDefL = [ktgis.FieldDef('name',fieldDefD)]
                
                # Create a shape file for all individual tiles
                tarDS, tarLayer = ktgis.ESRICreateDSLayer(dstFPN, spatialRef.proj_cs, 'polygon', 'tiles', fieldDefL)
                 
            iniTile = False  
            
            polytilegeom = ktgis.ShapelyPolyGeom([ul, ur, lr, ll])

            polytilegeom.ShapelyToOgrGeom()

            #create target feature
            tarFeat = ktgis.ogrFeature(tarLayer)
            
            fieldDefD = {'type':'string','transfer':'constant','source':tileFN,'width':8}

            fieldDefL = [ktgis.FieldDef('name',fieldDefD)]
            
            tarFeat.CreateOgrFeature(polytilegeom.ogrGeom, fieldDefL) 
            

   
        SNULLE
            
    else:
            
        BULLE

            
def PolyFromList():
    '''
    '''

    latlonProj = Proj('epsg:4326') # 4326 represents geographic coordinates

    projstr = 'epsg:%(e)d' %{'e':eD[easegrid]}
    # Set the target projection (EASE-grid)
    easeProj = Proj(projstr) # 6933 represents the global/tropial EASE grid

    session = ManageEASEgrid(db)

    home = path.expanduser("~")

    Ease2proj = ktgis.MjProj()

    Ease2proj.SetFromEPSG(eD[easegrid])

    # Create a shape file for all individual tiles in Geographic coordinates
    FN = '%(e)stiles-multi_karttur_epsg%(e)s.shp' %{'e': eD[easegrid]}

    tarShpFPN = path.join(home,FN)

    fieldDefD = {'type':'string','transfer':'constant','source':'globe','width':8}

    fieldDefL = [ktgis.FieldDef('name',fieldDefD)]

    # Create a shape file for all individual tiles
    tarDS,tarLayer = ktgis.ESRICreateDSLayer(tarShpFPN, Ease2proj.proj_cs, 'polygon', 'tiles', fieldDefL)

    # Define the side of a tile
    tileside = 900000

    # Set initial maxx
    maxx = -9000000

    for x in range(20):

        maxx += tileside

        minx = maxx-tileside

        maxy = -9000000

        for y in range(20):

            maxy += tileside

            miny = maxy-tileside

            ptL = [(minx,maxy),(maxx,maxy),(maxx,miny),(minx,miny)]

            tilegeom = ktgis.ShapelyPolyGeom(ptL)

            #convert to ogr
            tilegeom.ShapelyToOgrGeom()

            if x < 10:

                xtile = 'x0%s' %(x)

            else:

                xtile = 'x%s' %(x)

            if y < 10:

                ytile = 'y0%s' %(y)

            else:

                ytile = 'y%s' %(y)

            xytile = '%s%s' %(xtile,ytile)

            fieldDefD = {'type':'string','transfer':'constant','source':xytile,'width':8}

            fieldDefL = [ktgis.FieldDef('name',fieldDefD)]

            #create target feature
            tarFeat = ktgis.ogrFeature(tarLayer)

            tarFeat.CreateOgrFeature(tilegeom.ogrGeom, fieldDefL)


            west,south,east,north = tilegeom.shapelyGeom.bounds

            corners = ['ul','ur','lr','ll']

            llD = {}
            for z, pt in enumerate(ptL):

                lat,lon = transform(easeProj, latlonProj, pt[0], pt[1])
                key = '%(c)slat' %{'c':corners[z]}
                llD[key] = round(lat,5)

                key = '%(c)slon' %{'c':corners[z]}
                llD[key] = round(lon,5)

            # Write tile to db
            session._InsertTileCoord(easegrid,xytile,x,y,round(minx,2),round(maxy,2),round(maxx,2),
                                round(miny,2),round(west,2),round(south,2),round(east,2),round(north,2),
                                llD['ullat'],llD['ullon'],llD['lrlat'],llD['lrlon'],llD['urlat'],llD['urlon'],llD['lllat'],llD['lllon'])

            query = {'system':easegrid,'easegrid': easegrid, 'table':'regions','xtile':x,'ytile':y,'xytile':xytile,'regionid':'global','regioncat':'global','regiontype':'default','delete':False}

            session._InsertRegionTile(query)

    tarDS.CloseDS()

    if verbose > 0:

        print ('Check the shape file',tarShpFPN)