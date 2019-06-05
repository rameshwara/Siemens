import rhinoscriptsyntax as rs
import os

"""
1. Create multiple sphere, cylinder, cuboid, cone
2. Delete objects using ID
3. Move objects
4. Rotate objects
5. Scale objects

rs.AddSphere(center=(x,y,z), radius)
rs.AddBox([(x,y,z),(x,y,z),(x,y,z),(x,y,z),(x,y,z),(x,y,z),(x,y,z),(x,y,z)])
(Just take one point, length, width and height of box)
rs.AddCylinder(base=(x,y,z), height=(x,y,z), radius=Float, cap=True)
rs.AddCone(base=(x,y,z), height=(x,y,z), radius=Float, cap=True)
rs.DeleteObject(ID)
rs.MoveObject(ID, translation=(xdiff,ydiff,zdiff))
rs.RotateObject(ID, centerOfRotation=(x,y,z), angleInDeg=Float, axis=Int)
rs.ScaleObject(ID, scaleOrigin=(x,y,z), scale=[x,y,z])

"""

spheres, boxes, cylinders, cones = [], [], [], []

rs.Command("_-New None", True)

command = raw_input("Hello, I'm a chatbot for CAD modelling here in Rhino. How may I help you? ")

def createSphere():
    sphereRadius = rs.GetReal(message='Of what radius? ', minimum=0.1)
    x, y, z = [float(n) for n in raw_input('where?: "x y z"').split()]
    id = rs.AddSphere((x,y,z), sphereRadius)
    spheres.append(id)
    rs.SetUserText(id, key="Sphere", value=str(len(spheres)))
    print('Done.')

def createBox():
    l, b, h = [float(n) for n in raw_input('Of what dimensions?: "length breadth height"').split()]
    x, y, z = [float(n) for n in raw_input('where?: "x y z"').split()]
    id = rs.AddBox([(x,y,z),(x,y+b,z),(x+l,y+b,z),(x+l,y,z),(x,y,z+h),(x,y+b,z+h),(x+l,y+b,z+h),(x+l,y,z+h)])
    boxes.append(id)
    rs.SetUserText(id, key="Box", value=str(len(boxes)))
    print('Done.')

def createCylinder():
    cylinderRadius = rs.GetReal(message='Of what radius? ', minimum=0.1)
    x1, y1, z1 = [float(n) for n in raw_input('From where?: "x y z"').split()]
    x2, y2, z2 = [float(n) for n in raw_input('To where?: "x y z"').split()]
    id = rs.AddCylinder((x1,y1,z1), (x2,y2,z2), cylinderRadius, cap=True)
    cylinders.append(id)
    rs.SetUserText(id, key="Cylinder", value=str(len(cylinders)))
    print('Done.')

def createCone():
    coneRadius = rs.GetReal(message='Of what radius? ', minimum=0.1)
    x1, y1, z1 = [float(n) for n in raw_input('From where?: "x y z"').split()]
    x2, y2, z2 = [float(n) for n in raw_input('To where?: "x y z"').split()]
    id = rs.AddCone((x1,y1,z1), (x2,y2,z2), coneRadius, cap=True)
    cones.append(id)
    rs.SetUserText(id, key="Cone", value=str(len(cones)))
    print('Done.')

def moveObject(id):
    x, y, z = [float(n) for n in raw_input('To where?: "x y z"').split()]
    rs.MoveObject(id, (x,y,z))
    print('Done.')
    nextAction = ''
    
def rotateObject(id):
    angle = float(raw_input('By what angle (in degrees)?'))
    x, y, z = [float(n) for n in raw_input('At what point? Select the point carefully!: "x y z"').split()]
    X, Y, Z = [float(n) for n in raw_input('About what axis? "x y z": (Enter 1 to rotate or 0 to not rotate along a particular axis)').split()]
    rs.RotateObject(id, (x,y,z), angle, axis=(X,Y,Z))
    print('Done.')
    nextAction = ''
    
def scaleObject(id):
    x, y, z = [float(n) for n in raw_input('At what point? Select the point carefully!: "x y z"').split()]
    X, Y, Z = [float(n) for n in raw_input('By what factor? "x y z": (Scale factor for each axis. Enter 1 to retain original scale. Never enter 0.)').split()]
    rs.ScaleObject(id, (x,y,z), (X,Y,Z))
    print('Done.')
    nextAction = ''

def SaveAsRhinoFile(name="chatbotModel.3dm"):
    filename = name
    folder = 'C:/Users/Anna Reithmeir/PycharmProjects/rhinoChatbot/'
    path = os.path.abspath(folder + filename)
    cmd = "_-SaveAs " + chr(34) + path + chr(34)
    rs.Command(cmd, True)

nextAction = ''

while True:
    if ('create' in command) or ('create' in nextAction):
        if ('sphere' in command) or ('sphere' in nextAction):
            createSphere()
        elif ('box' in command) or ('box' in nextAction):
            createBox()
        elif ('cylinder' in command) or ('cylinder' in nextAction):
            createCylinder()
        elif ('cone' in command) or ('cone' in nextAction):
            createCone()
        else:
            object = rs.GetString(message='What do you want to create? Sphere, Box, Cylinder or Cone? ')
            if object == 'sphere':
                createSphere()
            elif object == 'box':
                createBox()
            elif object == 'cylinder':
                createCylinder()
            elif object == 'cone':
                createCone()
            else:
                print('Invalid choice')
    
    if ('delete' in command) or ('delete' in nextAction):
        if (len(spheres) == 0) and (len(boxes) == 0) and (len(cylinders) == 0) and (len(cones) == 0):
            print('There is no object to delete. Please create one or some before trying to delete.')
        else:
            if ('sphere' in command) or ('sphere' in nextAction):
                id = rs.GetObject(message='Double click on the sphere to delete on any view')
                if id in spheres: 
                    spheres.remove(id)
                    rs.DeleteObject(id)
                elif id in boxes:
                    deleteObj = raw_input('That is a Box. Do you still want to delete it?')
                    if deleteObj == 'yes': 
                        rs.DeleteObject(id)
                        boxes.remove(id)
                elif id in cylinders:
                    deleteObj = raw_input('That is a Cylinder. Do you still want to delete it?')
                    if deleteObj == 'yes': 
                        rs.DeleteObject(id)
                        cylinders.remove(id)
                elif id in cones:
                    deleteObj = raw_input('That is a Cone. Do you still want to delete it?')
                    if deleteObj == 'yes': 
                        rs.DeleteObject(id)
                        cones.remove(id)
                else: print('Unidentified sphere. Failed to delete.')
            elif ('box' in command) or ('box' in nextAction):
                id = rs.GetObject(message='Double click on the box to delete on any view')
                if id in boxes: 
                    boxes.remove(id)
                    rs.DeleteObject(id)
                elif id in spheres:
                    deleteObj = raw_input('That is a Sphere. Do you still want to delete it?')
                    if deleteObj == 'yes': 
                        rs.DeleteObject(id)
                        spheres.remove(id)
                elif id in cylinders:
                    deleteObj = raw_input('That is a Cylinder. Do you still want to delete it?')
                    if deleteObj == 'yes': 
                        rs.DeleteObject(id)
                        cylinders.remove(id)
                elif id in cones:
                    deleteObj = raw_input('That is a Cone. Do you still want to delete it?')
                    if deleteObj == 'yes': 
                        rs.DeleteObject(id)
                        cones.remove(id)
                else: print('Unidentified box. Failed to delete.')
            elif ('cylinder' in command) or ('cylinder' in nextAction):
                id = rs.GetObject(message='Double click on the cylinder to delete on any view')
                if id in cylinders: 
                    cylinders.remove(id)
                    rs.DeleteObject(id)
                elif id in spheres:
                    deleteObj = raw_input('That is a Sphere. Do you still want to delete it?')
                    if deleteObj == 'yes': 
                        rs.DeleteObject(id)
                        spheres.remove(id)
                elif id in boxes:
                    deleteObj = raw_input('That is a Box. Do you still want to delete it?')
                    if deleteObj == 'yes': 
                        rs.DeleteObject(id)
                        boxes.remove(id)
                elif id in cones:
                    deleteObj = raw_input('That is a Cone. Do you still want to delete it?')
                    if deleteObj == 'yes': 
                        rs.DeleteObject(id)
                        cones.remove(id)
                else: print('Unidentified cylinder. Failed to delete.')
            elif ('cone' in command) or ('cone' in nextAction):
                id = rs.GetObject(message='Double click on the cone to delete on any view')
                if id in cones: 
                    cones.remove(id)
                    rs.DeleteObject(id)
                elif id in spheres:
                    deleteObj = raw_input('That is a Sphere. Do you still want to delete it?')
                    if deleteObj == 'yes': 
                        rs.DeleteObject(id)
                        spheres.remove(id)
                elif id in cylinders:
                    deleteObj = raw_input('That is a Cylinder. Do you still want to delete it?')
                    if deleteObj == 'yes': 
                        rs.DeleteObject(id)
                        cylinders.remove(id)
                elif id in boxes:
                    deleteObj = raw_input('That is a Box. Do you still want to delete it?')
                    if deleteObj == 'yes': 
                        rs.DeleteObject(id)
                        boxes.remove(id)
                else: print('Unidentified cone. Failed to delete.')
            else:
                id = rs.GetObject(message='Double click on the object to delete on any view')
                if id in spheres:
                    spheres.remove(id)
                    rs.DeleteObject(id)
                elif id in boxes:
                    boxes.remove(id)
                    rs.DeleteObject(id)
                elif id in cylinders:
                    cylinders.remove(id)
                    rs.DeleteObject(id)
                elif id in cones:
                    cones.remove(id)
                    rs.DeleteObject(id)
                else:
                    print('Unidentified object. Failed to delete.')
            
    if ('move' in command) or ('move' in nextAction):
        if (len(spheres) == 0) and (len(boxes) == 0) and (len(cylinders) == 0) and (len(cones) == 0):
            print('There is no object to move. Please create one or some before trying to move.')
        else:
            if ('sphere' in command) or ('sphere' in nextAction):
                id = rs.GetObject(message='Double click on the sphere to move on any view')
                moveObject(id)
            elif ('box' in command) or ('box' in nextAction):
                id = rs.GetObject(message='Double click on the box to move on any view')
                moveObject(id)
            elif ('cylinder' in command) or ('cylinder' in nextAction):
                id = rs.GetObject(message='Double click on the cylinder to move on any view')
                moveObject(id)
            elif ('cone' in command) or ('cone' in nextAction):
                id = rs.GetObject(message='Double click on the cone to move on any view')
                moveObject(id)
            else:
                id = rs.GetObject(message='Double click on the object to move on any view')
                moveObject(id)
    
    if ('rotate' in command) or ('rotate' in nextAction):
        if (len(spheres) == 0) and (len(boxes) == 0) and (len(cylinders) == 0) and (len(cones) == 0):
            print('There is no object to rotate. Please create one or some before trying to rotate.')
        else:
            if ('sphere' in command) or ('sphere' in nextAction):
                id = rs.GetObject(message='Double click on the sphere to rotate on any view')
                rotateObject(id)
            elif ('box' in command) or ('box' in nextAction):
                id = rs.GetObject(message='Double click on the box to rotate on any view')
                rotateObject(id)
            elif ('cylinder' in command) or ('cylinder' in nextAction):
                id = rs.GetObject(message='Double click on the cylinder to rotate on any view')
                rotateObject(id)
            elif ('cone' in command) or ('cone' in nextAction):
                id = rs.GetObject(message='Double click on the cone to rotate on any view')
                rotateObject(id)
            else:
                id = rs.GetObject(message='Double click on the object to rotate on any view')
                rotateObject(id)
                
    if ('scale' in command) or ('scale' in nextAction):
        if (len(spheres) == 0) and (len(boxes) == 0) and (len(cylinders) == 0) and (len(cones) == 0):
            print('There is no object to scale. Please create one or some before trying to scale.')
        else:
            if ('sphere' in command) or ('sphere' in nextAction):
                id = rs.GetObject(message='Double click on the sphere to scale on any view')
                scaleObject(id)
            elif ('box' in command) or ('box' in nextAction):
                id = rs.GetObject(message='Double click on the box to scale on any view')
                scaleObject(id)
            elif ('cylinder' in command) or ('cylinder' in nextAction):
                id = rs.GetObject(message='Double click on the cylinder to scale on any view')
                scaleObject(id)
            elif ('cone' in command) or ('cone' in nextAction):
                id = rs.GetObject(message='Double click on the cone to scale on any view')
                scaleObject(id)
            else:
                id = rs.GetObject(message='Double click on the object to scale on any view')
                scaleObject(id)
    
    if ('save' in command) or ('save' in nextAction):
        filename = raw_input('What would you like to save the file as?')
        SaveAsRhinoFile(filename+'.3dm')
        print('File has been saved.')
        
    if ('quit' in command) or ('quit' in nextAction):
        filename = raw_input('What would you like to save the file as?')
        if filename == 'none':
            print('Quitting without saving.')
            break
        else:
            SaveAsRhinoFile(filename+'.3dm')
            print('File has been saved. Quitting now.')
            break
        
    command = ''
    print('SUMMARY - Spheres: %d, Boxes: %d, Cylinders: %d, Cones: %d' % (len(spheres), len(boxes), len(cylinders), len(cones)))
    nextAction = raw_input('What do you want to do next? ')