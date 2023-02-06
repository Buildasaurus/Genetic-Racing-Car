class Information
{
  int generation = 1;
  int totalfitness = 0;
  
  void display(int g, int tf)
  {
    generation = g;
    totalfitness = tf;
    fill(0);
    textSize(30);
    text("generation: " + generation, 10, height-40);
    text("Samlet fitness: " + totalfitness, 10, height-10);
    
    if (pile)
    {
      fill(0,200,0);
      text("Sensorer synlig(M)", width-250, height-10);
    } else
    {
      fill(200,0,0);
      text("Sensorer usynlig(M)", width-250, height-10);
    }
  }
}
