class SensorSystem {
  //SensorSystem - alle bilens sensorer - ogå dem der ikke bruges af "hjernen"
  
  //wall detectors
  int sensorMag = 50;
  float sensorAngle = PI*2/8;
  
  PVector anchorPos           = new PVector();
  
  PVector sensorVectorFront   = new PVector(0, sensorMag);
  PVector sensorVectorLeft    = new PVector(0, sensorMag);
  PVector sensorVectorRight   = new PVector(0, sensorMag);

  int frontSensorSignal;
  int leftSensorSignal;
  int rightSensorSignal;

  //crash detection
  int whiteSensorFrameCount    = 0; //udenfor banen

  //clockwise rotation detection
  PVector centerToCarVector     = new PVector();
  float   lastRotationAngle   = -1;
  float   clockWiseRotationFrameCounter  = 0;

  //lapTime calculation
  boolean lastGreenDetection;
  int     lastTimeInFrames      = 0;
  int     lapTimeInFrames       = 10000;

  void displaySensors() {
    strokeWeight(0.5);
    fill(255, 0, 0);
    ellipse(anchorPos.x+sensorVectorFront.x*frontSensorSignal/sensorMag, anchorPos.y+sensorVectorFront.y*frontSensorSignal/sensorMag, 8, 8);
    ellipse( anchorPos.x+sensorVectorLeft.x*leftSensorSignal/sensorMag, anchorPos.y+sensorVectorLeft.y*leftSensorSignal/sensorMag, 8, 8);
    ellipse( anchorPos.x+sensorVectorRight.x*rightSensorSignal/sensorMag, anchorPos.y+sensorVectorRight.y*rightSensorSignal/sensorMag, 8, 8);
    line(anchorPos.x, anchorPos.y, anchorPos.x+sensorVectorFront.x*frontSensorSignal/sensorMag, anchorPos.y+sensorVectorFront.y*frontSensorSignal/sensorMag);
    line(anchorPos.x, anchorPos.y, anchorPos.x+sensorVectorLeft.x*leftSensorSignal/sensorMag, anchorPos.y+sensorVectorLeft.y*leftSensorSignal/sensorMag);
    line(anchorPos.x, anchorPos.y, anchorPos.x+sensorVectorRight.x*rightSensorSignal/sensorMag, anchorPos.y+sensorVectorRight.y*rightSensorSignal/sensorMag);

    strokeWeight(2);
    if (whiteSensorFrameCount>0) {
      fill(whiteSensorFrameCount*10, 0, 0);
    } else {
      fill(0, clockWiseRotationFrameCounter, 0);
    }
    ellipse(anchorPos.x, anchorPos.y, 10, 10);
  }

  void updateSensorsignals(PVector pos, PVector vel) {
    //Collision detectors
    for (int i=1; i < sensorMag; i++)
    {
      PVector bob = sensorVectorFront;
      if (get(int(pos.x+bob.x*i/sensorMag), int(pos.y+bob.y*i/sensorMag))==-1)
      {
        frontSensorSignal = i;
        if (i==1)
        {
          frontSensorSignal = sensorMag;
        }
        i = sensorMag;
      } 
      else {frontSensorSignal = sensorMag;}
    }
     for (int i=1; i < sensorMag; i++)
    {
      PVector bob = sensorVectorLeft;
      if (get(int(pos.x+bob.x*i/sensorMag), int(pos.y+bob.y*i/sensorMag))==-1)
      {
        leftSensorSignal = i;
        if (i==1)
        {
          leftSensorSignal = sensorMag;
        }
        i = sensorMag;
      } 
      else {leftSensorSignal = sensorMag;}
    }
    for (int i=1; i < sensorMag; i++)
    {
      PVector bob = sensorVectorRight;
      if (get(int(pos.x+bob.x*i/sensorMag), int(pos.y+bob.y*i/sensorMag))==-1)
      {
        rightSensorSignal = i;
        if (i==1)
        {
          rightSensorSignal = sensorMag;
        }
        i = sensorMag;
      } 
      else {rightSensorSignal = sensorMag;}
    }  
    //Crash detector
    color color_car_position = get(int(pos.x), int(pos.y));
    if (color_car_position ==-1) {
      whiteSensorFrameCount = whiteSensorFrameCount+1;
    }
    //Laptime calculation
    boolean currentGreenDetection =false;
    if (red(color_car_position)==0 && blue(color_car_position)==0 && green(color_car_position)!=0) {//den grønne målstreg er detekteret
      currentGreenDetection = true;
    }
    if (lastGreenDetection && !currentGreenDetection) {  //sidst grønt - nu ikke -vi har passeret målstregen 
      lapTimeInFrames = frameCount - lastTimeInFrames; //LAPTIME BEREGNES - frames nu - frames sidst
      lastTimeInFrames = frameCount;
    }   
    lastGreenDetection = currentGreenDetection; //Husker om der var grønt sidst
    //count clockWiseRotationFrameCounter
    centerToCarVector.set((height/2)-pos.x, (width/2)-pos.y);    
    float currentRotationAngle =  centerToCarVector.heading();
    float deltaHeading   =  lastRotationAngle - centerToCarVector.heading();
    clockWiseRotationFrameCounter  =  deltaHeading>0 ? clockWiseRotationFrameCounter + 1 : clockWiseRotationFrameCounter -1;
    lastRotationAngle = currentRotationAngle;
    
    updateSensorVectors(vel);
    
    anchorPos.set(pos.x,pos.y);
  }

  void updateSensorVectors(PVector vel) {
    if (vel.mag()!=0) {
      sensorVectorFront.set(vel);
      sensorVectorFront.normalize();
      sensorVectorFront.mult(sensorMag);
    }
    sensorVectorLeft.set(sensorVectorFront);
    sensorVectorLeft.rotate(-sensorAngle);
    sensorVectorRight.set(sensorVectorFront);
    sensorVectorRight.rotate(sensorAngle);
  }
}
