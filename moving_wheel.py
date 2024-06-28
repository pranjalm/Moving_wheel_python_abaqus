from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import os
#creating a model
model_names = ['fric_04']
# 'fric_04', 'fric_05', 'fric_07', 'fric_08','fric_09', 'fric_06','fric_10', 'fric_03', 'tran_03','fric_10'
for model_name in model_names:
    if model_name in mdb.models.keys():
        del mdb.models[model_name] 

for model_name in model_names:
    # creating model from the list-model_names     
    mdb.Model(name=model_name, modelType=STANDARD_EXPLICIT)
    # assign parameter values from model names
    fric = float(model_name[-2:])/10 
    #elastic materials	
    el_mat = {'steel':[(7850.0, ), (200000000000.0, 0.3)], 'sleeper':[(2400.0, ), (30000000000.0, 0.2)] ,
            'ballast':[(2400.0, ), (140000000.0, 0.37)], 'subgrade':[(2000.0, ), (30000000.0, 0.4)] ,
            'subballast':[(2400.0, ), (70000000.0, 0.37)]}
    for i,j in el_mat.items():
        #soil material
        mdb.models[model_name].Material(name=i)
        mdb.models[model_name].materials[i].Density(table=(j[0], ))
        mdb.models[model_name].materials[i].Elastic(table=(j[1], ))

    lngth = 199.8 # extrusion length of the substructure layer
     
    #ballast sketch # Long part 1
    s = mdb.models[model_name].ConstrainedSketch(name='ballast', sheetSize=20)
    s.Line(point1=(3.65, 4.0), point2=(6.125, 4.0))
    s.Line(point1=(6.125, 4.0), point2=(6.125, 4.35))
    s.Line(point1=(6.125, 4.35), point2=(4.35, 4.35))
    s.Line(point1=(4.35, 4.35), point2=(3.65, 4.0))

    #subballast sketch # Long part 2
    s = mdb.models[model_name].ConstrainedSketch(name='subballast', sheetSize=20)
    s.Line(point1=(0.25, 3.0), point2=(6.125, 3.0))
    s.Line(point1=(6.125, 3.0), point2=(6.125, 4.0))
    s.Line(point1=(6.125, 4.0), point2=(2.25, 4.0))
    s.Line(point1=(2.25, 4.0), point2=(0.25, 3.0))

    #subgrade sketch # Long part 3
    s = mdb.models[model_name].ConstrainedSketch(name='subgrade', sheetSize=20)
    s.Line(point1=(-3.75, -7.0), point2=(6.125, -7.0))
    s.Line(point1=(6.125, -7.0), point2=(6.125, 3.0))
    s.Line(point1=(6.125, 3.0), point2=(-3.75, 3.0))
    s.Line(point1=(-3.75, 3.0), point2=(-3.75, -7.0))

    #rail sketch # Long part 4
    s = mdb.models[model_name].ConstrainedSketch(name='rail', sheetSize=0.2)
    s.Line(point1=(0, 0), point2=(0.15, 0))
    s.Line(point1=(0.15, 0), point2=(0.15, 0.02))
    s.Line(point1=(0.15, 0.02), point2=(0.1, 0.02))
    s.Line(point1=(0.1, 0.02), point2=(0.1, 0.07))
    s.Line(point1=(0.1, 0.07), point2=(0.05, 0.07))
    s.Line(point1=(0.05, 0.07), point2=(0.05, 0.02))
    s.Line(point1=(0.05, 0.02), point2=(0, 0.02))
    s.Line(point1=(0, 0.02), point2=(0, 0))

    #long parts (rail, ballast, subballast, subgrade)
    for i in mdb.models[model_name].sketches.keys():
        p = mdb.models[model_name].Part(dimensionality=THREE_D, name=i, type= DEFORMABLE_BODY)
        p.BaseSolidExtrude(sketch=mdb.models[model_name].sketches[i], depth=lngth)

    #infi_1 sketch # infi part 1
    s = mdb.models[model_name].ConstrainedSketch(name='infi_1', sheetSize=20)
    s.Line(point1=(-3.75, -7.0), point2=(6.125, -7.0))
    s.Line(point1=(6.125, -7.0), point2=(6.125, 4.35))
    s.Line(point1=(6.125, 4.35), point2=(4.35, 4.35))
    s.Line(point1=(4.35, 4.35), point2=(3.65, 4.0))
    s.Line(point1=(3.65, 4.0), point2=(2.25, 4.0))
    s.Line(point1=(2.25, 4.0), point2=(0.25, 3.0))
    s.Line(point1=(0.25, 3.0), point2=(-3.75, 3.0))
    s.Line(point1=(-3.75, 3.0), point2=(-3.75, -7.0))

    #infi_long sketch # infi part 2
    s = mdb.models[model_name].ConstrainedSketch(name='infi_long', sheetSize=20)
    s.Line(point1=(-4.75, -7.0), point2=(-3.75, -7.0))
    s.Line(point1=(-3.75, -7.0), point2=(-3.75, 3.0))
    s.Line(point1=(-3.75, 3.0), point2=(-4.75, 3.0))
    s.Line(point1=(-4.75, 3.0), point2=(-4.75, -7.0))

    #infi_bot sketch # infi part 3
    s = mdb.models[model_name].ConstrainedSketch(name='infi_bot', sheetSize=20)
    s.Line(point1=(-3.75, -8.0), point2=(6.125, -8.0))
    s.Line(point1=(6.125, -8.0), point2=(6.125, -7.0))
    s.Line(point1=(6.125, -7.0), point2=(-3.75, -7.0))
    s.Line(point1=(-3.75, -7.0), point2=(-3.75, -8.0))

    #sleeper sketch # Lateral part 1
    s_sleeper = mdb.models[model_name].ConstrainedSketch(name='sleeper', sheetSize=0.4)
    s_sleeper.Line(point1=(0, 0), point2=(0.25, 0))
    s_sleeper.Line(point1=(0.25, 0), point2=(0.2, 0.21))
    s_sleeper.Line(point1=(0.2, 0.21), point2=(0.05, 0.21))
    s_sleeper.Line(point1=(0.05, 0.21), point2=(0, 0))

    #wheel sketch # Lateral part 2
    s_wheel = mdb.models[model_name].ConstrainedSketch(name='wheel', sheetSize=1.0)
    s_wheel.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0, -0.5))
    
    #sleeper part
    p = mdb.models[model_name].Part(name='sleeper', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p.BaseSolidExtrude(sketch=s_sleeper, depth=1.2175)

    #wheel part
    p = mdb.models[model_name].Part(name='wheel', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p.BaseSolidExtrude(sketch=s_wheel, depth=0.05)

    #infi_1 part
    #p = mdb.models[model_name].Part(name='infi_1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    #p.BaseSolidExtrude(sketch=s_inf, depth=1)

    #Creating main sections of parts
    for i in mdb.models[model_name].parts.keys():
        p = mdb.models[model_name].parts[i]
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
        p.Set(cells=cells, name='main')

    # Assigning materials to the sections
    for i in mdb.models[model_name].materials.keys():
        mdb.models[model_name].HomogeneousSolidSection(name=i+'_section',material=i, thickness=None)

    # Section assignments to the individual parts
    for i in mdb.models[model_name].parts.keys():
        if(i in ['rail', 'wheel']):
            p = mdb.models[model_name].parts[i]
            p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region= p.sets['main'],
                            sectionName='steel_section', thicknessAssignment=FROM_SECTION)
        else:
            p = mdb.models[model_name].parts[i]
            p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region= p.sets['main'],
                            sectionName=i+'_section', thicknessAssignment=FROM_SECTION)
    
    #Creating surfaces for intraction ballast and subgrade
    for i in ['ballast', 'subballast','subgrade']:
        p = mdb.models[model_name].parts[i]
        s = p.faces
        if(i== 'subgrade'):
            p.Set(faces=s.getSequenceFromMask(mask=('[#4 ]', ), ), name='bottom')
        else:
            p.Surface(side1Faces=s.getSequenceFromMask(mask=('[#4]', ), ), name='bottom')
        p.Surface(side1Faces=s.getSequenceFromMask(mask=('[#1]', ), ), name='top')
        
        p.Set(faces=s.getSequenceFromMask(mask=('[#10 ]', ), ), name='side1')
        p.Set(faces=s.getSequenceFromMask(mask=('[#20 ]', ), ), name='side2')
        p.Set(faces=s.getSequenceFromMask(mask=('[#2 ]', ), ), name='roller_long')

    # wheel surfaces    
    p = mdb.models[model_name].parts['wheel']
    s = p.faces
    p.Surface(side1Faces=s.getSequenceFromMask(mask=('[#1]', ), ), name='rim')

    # rail surfaces    
    p = mdb.models[model_name].parts['rail']
    s = p.faces
    p.Surface(side1Faces=s.getSequenceFromMask(mask=('[#40]', ), ), name='bottom')
    p.Surface(side1Faces=s.getSequenceFromMask(mask=('[#4]', ), ), name='top')
    p.Set(faces=s.getSequenceFromMask(mask=('[#100 ]', ), ), name='side1')
    p.Set(faces=s.getSequenceFromMask(mask=('[#200 ]', ), ), name='side2')

    # sleeper surfaces
    p = mdb.models[model_name].parts['sleeper']
    s = p.faces
    p.Surface(side1Faces=s.getSequenceFromMask(mask=('[#4]', ), ), name='bottom')
    p.Surface(side1Faces=s.getSequenceFromMask(mask=('[#1]', ), ), name='top')
    p.Set(faces=s.getSequenceFromMask(mask=('[#10 ]', ), ), name='roller_long')

    # Adding parts to assembly
    a = mdb.models[model_name].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    for i in mdb.models[model_name].parts.keys():
        p = mdb.models[model_name].parts[i]
        a.Instance(name=i+'-1', part=p, dependent=ON)
    
    # moving and rotating parts to adjust the assembaly 
    a.rotate(instanceList=('wheel-1', 'sleeper-1'), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 1.0, 0.0), angle=90.0)
    a.translate(instanceList=('sleeper-1', ), vector=(4.9075, 4.35, 0.125))
    a.translate(instanceList=('rail-1', ), vector=(5.212, 4.56, 0.0))
    a.translate(instanceList=('wheel-1', ), vector=(5.262, 5.13, 99.6))

    # creating sleepers pattern
    a.LinearInstancePattern(instanceList=('sleeper-1', ), direction1=(0.0, 0.0, 1.0), 
            direction2=(0.0, 1.0, 0.0), number1=334, number2=1, spacing1=0.6, spacing2=0.21)
    
    # Merging Sleepers into one instance
    a.InstanceFromBooleanMerge(name='sleepers', instances=tuple([i for i in a.instances.values() if 'sleeper' in i.name]), 
        keepIntersections=ON, originalInstances=DELETE, domain=GEOMETRY) 

    # Section assignment to sleepers
    p = mdb.models[model_name].parts['sleepers']
    p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region= p.sets['main'], 
                        sectionName='sleeper_section', thicknessAssignment=FROM_SECTION)
    
    #Creating tie conditions for the interactions
    mdb.models[model_name].Tie(adjust=ON, master=a.instances['ballast-1'].surfaces['bottom'], name='blt_sbt', 
        positionToleranceMethod=COMPUTED, slave=a.instances['subballast-1'].surfaces['top'], thickness=ON, 
        tieRotations=ON)

    mdb.models[model_name].Tie(adjust=ON, master=a.instances['subballast-1'].surfaces['bottom'], name='sbt_sbg', 
        positionToleranceMethod=COMPUTED, slave=a.instances['subgrade-1'].surfaces['top'], thickness=ON, 
        tieRotations=ON)

    mdb.models[model_name].Tie(adjust=ON, master=a.instances['sleepers-1'].surfaces['bottom'], name='slp_blt', 
        positionToleranceMethod=COMPUTED, slave=a.instances['ballast-1'].surfaces['top'], thickness=ON, 
        tieRotations=ON)
        
    mdb.models[model_name].Tie(adjust=ON, master=a.instances['rail-1'].surfaces['bottom'], name='rail_slp', 
        positionToleranceMethod=COMPUTED, slave=a.instances['sleepers-1'].surfaces['top'], thickness=ON, 
        tieRotations=ON)
    
    #Creating friction
    a = mdb.models[model_name].rootAssembly
    mdb.models[model_name].ContactProperty('friction_steel')
    mdb.models[model_name].interactionProperties['friction_steel'].TangentialBehavior( formulation=PENALTY, 
        directionality=ISOTROPIC, slipRateDependency=OFF, pressureDependency=OFF, temperatureDependency=OFF, 
        dependencies=0, table=((fric, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)
    mdb.models[model_name].interactionProperties['friction_steel'].NormalBehavior(pressureOverclosure=HARD, 
        allowSeparation=ON, constraintEnforcementMethod=DEFAULT)
    
    mdb.models[model_name].ContactProperty('fake')
    mdb.models[model_name].interactionProperties['fake'].TangentialBehavior(formulation=ROUGH)

    # general contact
    mdb.models[model_name].ContactExp(name='gen_cont', createStepName='Initial')
    mdb.models[model_name].interactions['gen_cont'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=ON)
    r21, r22 = a.instances['wheel-1'].surfaces['rim'], a.instances['rail-1'].surfaces['top']
    mdb.models[model_name].interactions['gen_cont'].contactPropertyAssignments.appendInStep(
        stepName='Initial', assignments=((GLOBAL, SELF, 'fake'), (r21, r22, 'friction_steel')))
    
    #Creating BC fixing the bottom
    region = a.allInstances['subgrade-1'].sets['bottom']
    mdb.models[model_name].EncastreBC(name='fixed', createStepName='Initial', region=region, localCsys=None)

    #Creating steps for the calculation
    mdb.models[model_name].ExplicitDynamicsStep(name='loading',timePeriod=1, previous='Initial')
    mdb.models[model_name].fieldOutputRequests['F-Output-1'].setValues(timeInterval=0.01, timeMarks=ON)
    mdb.models[model_name].historyOutputRequests['H-Output-1'].setValues(timeInterval=0.01)

    # creating gravity load
    mdb.models[model_name].Gravity(comp2=-9.81, createStepName='loading',distributionType=UNIFORM, field='', 
        name='gravity')
    
    # wheel partition
    p = mdb.models[model_name].parts['wheel']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e, v, d = p.edges, p.vertices, p.datums
    p.PartitionCellByPlaneNormalToEdge(edge=e[0], cells=pickedCells, point=p.InterestingPoint(edge=e[0], rule=MIDDLE))

    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#3 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e[0], cells=pickedCells, point=p.InterestingPoint(edge=e[0], rule=MIDDLE))

    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#f ]', ), )
    e, v, d = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e[0], cells=pickedCells, point=p.InterestingPoint(edge=e[0], rule=MIDDLE))

    # load application point
    verts = v.getSequenceFromMask(mask=('[#2 ]', ), )
    p.Set(vertices=verts, name='center')

    # creating point load at wheel 
    a = mdb.models[model_name].rootAssembly
    mdb.models[model_name].ConcentratedForce(name='wheel_load', createStepName='loading', 
                region=a.instances['wheel-1'].sets['center'], cf2=-162500.0, amplitude=UNSET, 
                distributionType=UNIFORM, field='', localCsys=None)

    region = a.instances['wheel-1'].sets['main']
    mdb.models[model_name].DisplacementBC(name='wheel', createStepName='Initial', 
        region=region, u1=SET, u2=UNSET, u3=SET, ur1=SET, ur2=SET, ur3=SET, 
        amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    amp_move = tuple([(i*0.01, i*0.1) for i in range(100)] )
    mdb.models[model_name].TabularAmplitude(name='move', timeSpan=STEP, 
        smooth=SOLVER_DEFAULT, data= amp_move)
    mdb.models[model_name].boundaryConditions['wheel'].setValuesInStep(
        stepName='loading', u3=30.0, amplitude='move')
    # Meshing
    msh = {'ballast':0.3,'subballast':0.3,'subgrade':0.6,'rail':0.15,'sleepers':0.2,'wheel':0.1}
    for k,v in msh.items():
        p = mdb.models[model_name].parts[k]
        p.seedPart(size=v, deviationFactor=0.1, minSizeFactor=0.1)
        p = mdb.models[model_name].parts[k]
        p.generateMesh()
    
    # create the job and write input file 
    mdb.Job(name=model_name+'_job', model=model_name, description='', type=ANALYSIS, atTime=None, waitMinutes=0, 
            waitHours=0, queue=None, memory=50, memoryUnits=PERCENTAGE, explicitPrecision=DOUBLE_PLUS_PACK, 
            nodalOutputPrecision=FULL, echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, 
            historyPrint=OFF, userSubroutine='', scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN,
            numDomains=16, activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=4)
    mdb.jobs[model_name+'_job'].writeInput(consistencyChecking=OFF)