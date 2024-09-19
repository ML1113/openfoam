#### import the simple module from the paraview
from paraview.simple import *
import os
import glob

def findLatestTime (FieldName,directory='.'):
    latestTime = -1.0
    listDirs = next(os.walk(directory))[1]
    for dirs in listDirs:
        print os.path.join(directory,dirs,FieldName)
        if os.path.exists(os.path.join(directory,dirs,FieldName)):
            if float(dirs) >  latestTime : latestTime = float(dirs)
    return latestTime


def plottingFunction(mfoamDisplay,renderView1,Field,lowerBound,upperBound,Component,listColor,listOpasi,FieldDict):
    
    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(pLUT, renderView1)
    
    timestepindex =  list(timesteps).index(FieldDict[Field])

    animationScene1.AnimationTime = timesteps[timestepindex]

    # show color bar/color legend
    mfoamDisplay.SetScalarBarVisibility(renderView1, True)

    # update the view to ensure updated data information
    renderView1.Update()

    # set scalar coloring
    ColorBy(mfoamDisplay, ('POINTS', Field, Component))
    
    
    if listColor:
        HideScalarBarIfNotNeeded(listColor[-1], renderView1)
    if listOpasi:
        HideScalarBarIfNotNeeded(listOpasi[-1], renderView1)

    # rescale color and/or opacity maps used to include current data range
    mfoamDisplay.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    mfoamDisplay.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'Vorticity_02'
    Field_02LUT = GetColorTransferFunction(Field)
    Field_02LUT.RGBPoints = [0.00011017243377864361, 0.231373, 0.298039, 0.752941, 1821.4325502034044, 0.865003, 0.865003, 0.865003, 3642.864990234375, 0.705882, 0.0156863, 0.14902]
    Field_02LUT.ScalarRangeInitialized = 1.0
    
    # get opacity transfer function/opacity map for 'Vorticity_02'
    Field_02PWF = GetOpacityTransferFunction(Field)
    Field_02PWF.Points = [-738.7027587890625, 0.0, 0.5, 0.0, 3642.864990234375, 1.0, 0.5, 0.0]
    Field_02PWF.ScalarRangeInitialized = 1

    # Rescale transfer function
    Field_02PWF.RescaleTransferFunction(lowerBound, upperBound)
    UpdateScalarBarsComponentTitle(Field_02PWF, mfoamDisplay)
    
    # Update a scalar bar component title.
    UpdateScalarBarsComponentTitle(Field_02LUT, mfoamDisplay)

    # Rescale transfer function
    Field_02LUT.RescaleTransferFunction(lowerBound, upperBound)

    # current camera placement for renderView1
    renderView1.CameraPosition = [0.0, 0.0, 0.6525264458313953]
    renderView1.CameraFocalPoint = [0.0, 0.0, 0.02500000037252903]
    renderView1.CameraParallelScale = 0.5097303410804502

    # save screenshot
    SaveScreenshot(Field+'.png', renderView1, ImageResolution=[938, 477])
    
    # show color bar/color legend
    mfoamDisplay.SetScalarBarVisibility(renderView1, False)
    
    listColor.append(Field_02LUT)
    listOpasi.append(Field_02PWF)
    
    

            
            
vorticityDict = {"Vorticity_0.2" : None, "Vorticity_0.64" : None,"Vorticity_1.24" : None,"Vorticity_1.6" : None,"Vorticity_1.8" : None}
UDict = {"U_0.2" : None, "U_0.64" : None,"U_1.24" : None,"U_1.6" : None,"U_1.8" : None}
pDict = {"p_0.2" : None, "p_0.64" : None,"p_1.24" : None,"p_1.6" : None,"p_1.8" : None}

for vorticity,U,p in zip(vorticityDict,UDict,pDict):
    vorticityDict[vorticity] = findLatestTime(vorticity)
    UDict[U] = findLatestTime(U)
    pDict[p] = findLatestTime(p)
    
print vorticityDict
print pDict
print UDict
    

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
mfoam = OpenFOAMReader(FileName='m.foam')
mfoam.MeshRegions = ['internalMesh']

variablesList = ['p' , 'U']

for vorticity,U,p in zip(vorticityDict,UDict,pDict):
    variablesList.append(vorticity)
    variablesList.append(U)
    variablesList.append(p)
    
mfoam.CellArrays = variablesList

# get animation scene
animationScene1 = GetAnimationScene()

# get time steps
tk = GetTimeKeeper()
timesteps = tk.TimestepValues
print timesteps


for vorticity in vorticityDict:
    print list(timesteps).index(vorticityDict[vorticity])

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [938, 477]

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')
pPWF = GetOpacityTransferFunction('p')

# show data in view
mfoamDisplay = Show(mfoam, renderView1)
# trace defaults for the display properties.

# reset view to fit data
renderView1.ResetCamera()

# show color bar/color legend
mfoamDisplay.SetScalarBarVisibility(renderView1, False)

# update the view to ensure updated data information
renderView1.Update()

listColor = [pLUT]
listOpasi = [pPWF]

for vorticity,U,p in zip(vorticityDict,UDict,pDict):
    plottingFunction(mfoamDisplay,renderView1,vorticity,-30,30,'Z',listColor,listOpasi,vorticityDict)
    plottingFunction(mfoamDisplay,renderView1,U,0,6.0,'Magnitude',listColor,listOpasi,UDict)
    plottingFunction(mfoamDisplay,renderView1,p,-10.0,10.0,'',listColor,listOpasi,pDict)
    
    
