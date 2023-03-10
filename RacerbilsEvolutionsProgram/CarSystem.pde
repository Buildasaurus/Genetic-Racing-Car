class CarSystem {
  //CarSystem - 
  //Her kan man lave en generisk alogoritme, der skaber en optimal "hjerne" til de forhåndenværende betingelser
  
  ArrayList<CarController> CarControllerList  = new ArrayList<CarController>();
  color[] farvestreger = {color(0,255,0), color(0,0,255),color(255,0,0),color(255,0,255),color(0,255,255)};
  Information information = new Information();
  float mutation = 0.02;
  int mutantChance = 20;
  float udenforstraf = 0.02;
  float bedsteBil = 0;
  

  CarSystem(int populationSize) 
  {
    for (int i=0; i<populationSize; i++) { 
      CarController controller = new CarController();
      CarControllerList.add(controller);
    }
  }
  
  void fitnessbestemmelse()
  {
    for (int i = 0; i < populationSize; i++) 
    {
      CarController controller = CarControllerList.get(i);
      color c = get(int(controller.bil.pos.x), int(controller.bil.pos.y));
      int nyC;
      int nyNyC;
      for (int j = 0; j < farvestreger.length; j++)
      {
        if (c == farvestreger[j])
        {
          nyC = j;
          if (nyC == 0)
          {
            nyNyC=farvestreger.length-1;
          }
          else 
          {
            nyNyC = nyC-1;
          }
          if (farvestreger[nyNyC] == controller.bil.lastpast)
          {
            controller.fitness = controller.fitness+1;
            if (controller.fitness > bedsteBil)
            {
              
              for (int k = 0; k < populationSize; k++) 
              {
                CarController controller2 = CarControllerList.get(k);
                controller2.sensorSystem.bedsteBil = false;
              }
              controller.sensorSystem.bedsteBil = true;
              bedsteBil = controller.fitness;
            } else
            {
              controller.sensorSystem.bedsteBil = false;
            }
            //println("Linje: " + j + " er paserset");
            controller.bil.lastpast = farvestreger[nyC];
            break;
          }
        } else if (c == -1)
        {
          controller.fitness = controller.fitness-0.01;
        }
      }
    }
  }
  
  void bedreBiler(ArrayList<CarController> _CarControllerList)
  {  
    information.generation++;
    information.totalfitness = 0;
    bedsteBil=0;
    //Laver en pulje hvorfra der kan blive trukket et nummer fra
    ArrayList<Integer> pulje = new ArrayList<Integer>();
    for (int i = 0; i < _CarControllerList.size(); i++)
    {
      CarController controller = _CarControllerList.get(i);
      for (int j = 0; j < int(pow(controller.fitness,1.5)); j++)
      {
        pulje.add(i);
      }
    }
   for (int i = 0; i < _CarControllerList.size(); i++)
    {
       CarController controller = _CarControllerList.get(i);
       information.totalfitness += controller.fitness;
    }
    println("Pulje lavet med " + pulje.size() +  " elementer");
    //Laver en ny generation baseret på den tidliger generation
    if (pulje.size() > 1) 
    {
      lavOgFjern(_CarControllerList, pulje);
    }
    else
    {
      lorteBiler(_CarControllerList);
    }
    
  }
  
  void lavOgFjern (ArrayList<CarController> _CarControllerList, ArrayList<Integer> pulje)
  {
    for (int i=0; i < populationSize; i++) 
    { 
      float[] weights = new float[10];
      float[] biases = {0,0,0,0}; 
      int[] Mamabil = {int(random(0, pulje.size())),int(random(0, pulje.size()))};
      while (Mamabil[0] == Mamabil[1])
      {
       Mamabil[1] = int(random(0, pulje.size()));
      }
      
      for (int j = 0; j < weights.length; j++) 
      {
          int mutantSker = int(random(1, mutantChance));
          int valgtGen = Mamabil[int(random(0 , 1))];
          CarController gamleBil = _CarControllerList.get(pulje.get(valgtGen));
          weights[j] = gamleBil.hjerne.weights[j];
          if (mutantSker == 1)
          {
            weights[j] = weights[j] + random(-mutation, mutation);
          }
        }
      for (int j=0; j < biases.length; j++) 
      {
        int valgtGen = Mamabil[int(random(0 , 1))];
        int mutantSker = int(random(1, mutantChance));
        CarController gamle = _CarControllerList.get(pulje.get(valgtGen));
        biases[j] = gamle.hjerne.biases[j];
        if (mutantSker == 1)
        {
          weights[j] = weights[j] + random(-mutation, mutation);
        }
      }
      CarController controller = new CarController(weights, biases);
      CarControllerList.add(controller);
    }
    
    for (int i = 0; i < populationSize; i++) 
    {
      _CarControllerList.remove(0);
    }
  }
  
  void lorteBiler (ArrayList<CarController> _CarControllerList)
  {
    for (int i = 0; i < populationSize; i++) 
    {
      _CarControllerList.remove(0);
    } 
    for (int i=0; i<populationSize; i++) { 
      CarController controller = new CarController();
      _CarControllerList.add(controller);
    }
    println("bilerne kunne ikke køre");
    
  }

  void updateAndDisplay() {
    //1.) Opdaterer sensorer og bilpositioner
    for (CarController controller : CarControllerList) {
      controller.update();
    } 
    image(forbillede,0,0,width,height);
    //2.) Tegner tilsidst - så sensorer kun ser banen og ikke andre biler!
    for (CarController controller : CarControllerList) {
      controller.display();
    }
  }
}
