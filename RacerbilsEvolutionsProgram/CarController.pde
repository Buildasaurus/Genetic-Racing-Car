class CarController {
  //Forbinder - Sensorer & Hjerne & Bil
  float varians             = 0.2; //hvor stor er variansen på de tilfældige vægte og bias
  Car bil                    = new Car();
  NeuralNetwork hjerne       = new NeuralNetwork(varians); 
  SensorSystem  sensorSystem = new SensorSystem();
      
  void update() {
    //1.)opdtarer bil 
    //2.)opdaterer sensorer    
    sensorSystem.updateSensorsignals(bil.pos, bil.vel);
    //3.)hjernen beregner hvor meget der skal drejes
    float turnAngle = 0;
    float x1 = int(sensorSystem.leftSensorSignal);
    float x2 = int(sensorSystem.frontSensorSignal);
    float x3 = int(sensorSystem.rightSensorSignal);    
    turnAngle = hjerne.getOutput(x1, x2, x3);    
    float nnu = hjerne.getPasta(x1, x2, x3);
    bil.update(nnu);
    //4.)bilen drejes
    bil.turnCar(turnAngle);
  }
  
  void display(){
    bil.displayCar();
    sensorSystem.displaySensors();
  }
}
