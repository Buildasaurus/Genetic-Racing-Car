class CarController {
  //Forbinder - Sensorer & Hjerne & Bil
  float varians             = 0.1; //hvor stor er variansen på de tilfældige vægte og bias
  Car bil                    = new Car();
  NeuralNetwork hjerne;
  SensorSystem  sensorSystem = new SensorSystem();
  float fitness = 0;
  
  CarController ()
  {
    hjerne = new NeuralNetwork(varians);
  }
  
  CarController (float[] _weights,float[] _biases)
  {
    hjerne = new NeuralNetwork(_weights, _biases);
  }
  
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
    sensorSystem.displaySensors();
  }
}
