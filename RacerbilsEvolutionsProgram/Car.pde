class Car {  
  //Bil - indeholder position & hastighed & "tegning"
  PVector pos = new PVector(535, 500);
  PVector vel = new PVector(0, -10);
  color lastpast = color(0,255,0);
  void turnCar(float turnAngle)
  {
    vel.rotate(turnAngle);
  }
  
  void update(float nnu) 
  {
    PVector Boef = new PVector(vel.x*nnu,vel.y*nnu);
    pos.add(Boef);
  }
  
}
