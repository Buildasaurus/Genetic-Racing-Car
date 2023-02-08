//populationSize: Hvor mange "controllere" der genereres, controller = bil & hjerne & sensorer
int     populationSize  = 100;     
boolean pile = true;
//CarSystem: Indholder en population af "controllere" 
CarSystem carSystem       = new CarSystem(populationSize);
Information information = new Information();

//trackImage: RacerBanen , Vejen=sort, Udenfor=hvid, Målstreg= 100%grøn 
PImage trackImage;
PImage forbillede;
PImage Racerbil1;
PImage Racerbil2;
PImage guldBil;
//PImage 

void setup() {
  size(1280, 720);
  trackImage = loadImage("Bagbillede.png");
  forbillede = loadImage("Forbillede.JPG");
  Racerbil1 = loadImage("Racerbil Rød.png");
  Racerbil2 = loadImage("Racerbil blå.png");
  guldBil = loadImage("Racerbil Guld.png");
}

void draw() {
  clear();
  fill(255);
  noStroke();
  rect(-300,-300,1000,1000);
  stroke(2);
  image(trackImage,0,0,width,height); 
  carSystem.fitnessbestemmelse();
  carSystem.updateAndDisplay();
  information.display(carSystem.information.generation, carSystem.information.totalfitness);
  if (frameCount%1500==0) 
  {
    //println("FJERN DEM DER KØRER UDENFOR BANEN frameCount: " + frameCount);
    carSystem.bedreBiler(carSystem.CarControllerList);
  }
      
  //TESTKODE: Frastortering af dårlige biler, for hver gang der går 200 frame - f.eks. dem der kører uden for banen
   
      /*
      for (int i = carSystem.CarControllerList.size()-1 ; i >= 0;  i--) {
        SensorSystem s = carSystem.CarControllerList.get(i).sensorSystem;
        if(s.whiteSensorFrameCount > 0){
          carSystem.CarControllerList.remove(carSystem.CarControllerList.get(i));
          //carSystem.NyCar();
         }
      }*/
}

void keyReleased()
{
  if (key =='m' || key =='M')
  {
   pile ^= true;
  }
}
