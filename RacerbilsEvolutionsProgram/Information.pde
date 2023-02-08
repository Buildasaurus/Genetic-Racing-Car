class Information
{
  int generation = 1;
  int totalfitness = 0;
  
  void display(int g, int tf)
  {
    generation = g;
    totalfitness = tf;
    fill(255);
    textSize(30);
    text("generation: " + generation, width-400, 50);
    text("Samlet fitness: " + totalfitness, width-400, 100);
    
    if (pile)
    {
      fill(0,200,0);
      text("Sensorer synlig(M)", width-400, 150);
    } else
    {
      fill(200,0,0);
      text("Sensorer usynlig(M)", width-400, 150);
    }
  }
}
