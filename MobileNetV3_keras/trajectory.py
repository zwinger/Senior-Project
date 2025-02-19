from math import sqrt, atan, sin, cos, pi

from numpy import median

class Trajectory:
   def __init__(self, width, height, num_outputs):
      self.width = width
      self.height = height
      self.num_outputs = num_outputs
      self.stepSize = width // num_outputs

      #Info regarding the robot's position in the image
      self.robotWidth = 50 #Represented in pixels
      self.robotCenter = ((self.width-1)//2, self.height-1)
      self.robotLeft = self.robotCenter[0] - self.robotWidth
      self.robotRight = self.robotCenter[0] + self.robotWidth
      self.robotFront = self.robotCenter[1] - 30 #Front of the robot
      self.robotCloseUp = self.robotCenter[1] - 15 #The very front of the robot
      self.maxTranslation = self.distance(self.robotCenter, (self.width, 0))

   def calculateTrajectory(self, prediction):
      highestPoint_X = [self.robotCenter[0]]
      highestPoint_Y = [self.robotCenter[1]]
      leftMax = self.robotCenter[1]
      rightMax = self.robotCenter[1]
      blocked = False

      x = 0
      for i in range(self.num_outputs):
         y = int(round(prediction[i] * (self.height)))

         #Find the set of furthest points away from the bottom of the image
         if y < min(highestPoint_Y) - 2:
            highestPoint_Y = [y]
            highestPoint_X = [x]
         elif y < min(highestPoint_Y) + 5 and y >= min(highestPoint_Y) - 2 and x - max(highestPoint_X) == self.stepSize:
            highestPoint_Y.append(y)
            highestPoint_X.append(x)

         #Get the furthest point away from the bottom to the left and right of 
         #the robot in case there's an obtacle
         if x < self.robotLeft and y < leftMax:
            leftMax = y
         elif x > self.robotRight and y < rightMax:
            rightMax = y

         #Determine if something is near the front of the robot
         if x in range(self.robotLeft, self.robotRight+1) and y >= self.robotFront:
            blocked = True
         x += self.stepSize

      magnitude = 0
      theta = 0
      if not blocked:
         highestPoint = (median(highestPoint_X), median(highestPoint_Y))
         #Calculate trajectory of the robot
         magnitude = self.distance(self.robotCenter, highestPoint)
         translation = magnitude / float(self.maxTranslation)
         diff_x = self.robotCenter[0] - highestPoint[0]
         diff_y = self.robotCenter[1] - highestPoint[1]
         theta = atan(diff_x / float(diff_y))
         rotation = theta / (pi / 2.0)

      else:
         translation = 0
         #Choose a direction to turn (left or right)
         #Turn Left, it's more clear than the right
         if leftMax < rightMax:
            rotation = 1
         #Turn Right, it's more clear than the left
         else:
            rotation = -1

      return (translation, rotation)

   '''Turn the given trajectory and rotaiton into the point to go towards'''
   def trajectoryToPoint(self, translation, rotation):
      theta = rotation * (pi / 2.0)
      mag = translation * self.maxTranslation
      translation_x = self.robotCenter[0] - int(mag * sin(theta))
      translation_y = self.robotCenter[1] - int(mag * cos(theta))
      return (translation_x, translation_y)

   '''Compute the Euclidean distance between 2 points'''
   def distance(self, p1, p2):
      return sqrt(((p1[0]-p2[0])**2.0) + ((p1[1]-p2[1])**2.0))