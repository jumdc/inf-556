#include <cstdlib>
#include <string.h>
#include <stdio.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <set>
#include <map>
#include <limits>
#include <assert.h>
#include <math.h>
#include <iterator>

using namespace std;


/*************
class Point{};
*************/


/*************
class Cover{};
**************/



typedef vector<Point> Cloud;
typedef map<Point, vector<Point> > Graph; //sparse matrix of adjacencies
typedef map<int, vector<Point> > ConnectedComp;


Cloud read_cloud(char* const & name){
  int dim; Cloud C; C.clear();
  ifstream input(name);
  if(input){
    string line; vector<double> coord; int ID = 0;
    while(getline(input,line)){
      coord.clear(); double x = numeric_limits<double>::max();
      stringstream stream(line);
      while(stream >> x){coord.push_back(x);}
      Point p = Point(ID, coord);
      if(x != numeric_limits<double>::max()){C.push_back(p); ID++;}
    }
  }
  else{cout << "Failed to read file " << name << endl; return C;}
  return C;
}

void read_function_from_file(char* const & name, Cloud & C){
  int num_pts = C.size(); double x;
  ifstream input(name);
  if(input){
    for(int i = 0; i < num_pts; i++)
      input >> C[i].func;
  }
  else{cout << "Failed to read file " << name << endl; return;}
  return;
}

void read_coordinate(const int & number, Cloud & C){
  int num_pts = C.size();
  for(int i = 0; i < num_pts; i++)
    C[i].func = C[i].coord[number];
  return;
}

Graph build_neighborhood_graph(const Cloud & C, const double & delta){

  int nb = C.size(); Graph G; G.clear(); vector<Point> adj; adj.clear(); double d; vector<vector<double> > dist; dist.clear();
  for(int i = 0; i < nb; i++)
    G.insert(pair<Point, vector<Point> >(C[i],adj));
  double m = 0; int k = 0;
  for(int i = 0; i < nb; i++){
    if( (int) floor( 100*((double) i)/((double) nb)+1 ) %10 == 0  ){cout << "\r" << floor( 100*((double) i)/((double) nb) +1) << "%" << flush;}
    vector<double> dis; dis.clear();
    for (int j = i+1; j < nb; j++){
      d = C[i].EuclideanDistance(C[j]); dis.push_back(d);
      if(m<=d){m = d;}
    }
    dist.push_back(dis);
  }
  cout << endl << "  Done." << endl << "  Building and printing neighborhood graph...  ";
  cout.flush();
  for(int i = 0; i < nb; i++){
    for (int j = i+1; j < nb; j++){
      if(dist[i][j-i-1] <= delta*m){
        G[C[i]].push_back(C[j]); G[C[j]].push_back(C[i]); k++;
      }
    }
  }
  cout << 100*((double) k)/((double) nb*(nb-1)/2) << "% of pairs selected." << endl;
  return G;
}



/**************************
To be completed
**************************/
ConnectedComp count_cc(Graph & G, int& id) {
  ConnectedComp res;
  return res;
}

/************************************
To be completed
************************************/
vector<ConnectedComp> MapperElts(Graph & G, Cover & I){
  vector<ConnectedComp> res;
  return res;
}

/*********************************************
To be completed
*********************************************/
map<int, vector<int> > build_mapper_graph(vector<ConnectedComp> & M){
  map<int, vector<int> > res;
  return res;
}



int main(int argc, char** argv){

  if(argc <= 9){cout << "Usage: <cloud_file> <function:/coordinate:> <func_file/number> <parameter:> <delta> <mask:> <number> <covering:> <resolution> <gain>" << endl; return 0;}
  if(argc >= 12){cout << "Too many arguments !" << endl; return 0;}

  char* const cloud = argv[1];
  char* const funct = argv[2];
  char* const graph = argv[4];
  int mask = atoi(argv[7]);
  char* const covering = argv[8];

  Cover I; Graph G; Cloud C; vector<ConnectedComp> M;

  cout << "Reading input cloud from file " << cloud << "..." << endl;
  C = read_cloud(cloud);
  cout << "  Done." << endl;

  if (strcmp(funct, "function:") == 0){
    char* const func = argv[3];
    cout << "Reading input filter from file " << func << "..." << endl;
    read_function_from_file(func,C);
  }
  else{
    int number = atoi(argv[3]);
    cout << "Using coordinate " << number << " as a filter..." << endl;
    read_coordinate(number,C);
  }
  cout << "  Done." << endl;

  double delta = atof(argv[5]);
  cout << "Computing neighborhood graph with delta parameter = " << delta << "..." << endl;
  G = build_neighborhood_graph(C, delta);
  cout << "  Done." << endl;

  double resolution = atoi(argv[9]);
  double gain = atof(argv[10]); assert (gain >= 0);
  cout << "Computing uniform covering with resolution " << resolution << " and gain " << gain << "..." << endl;
  I = Cover(C.begin()->func, (C.end()-1)->func, resolution, gain);
  cout << "  Done." << endl;

  cout << "Computing Mapper Elements..." << endl;
  M = MapperElts(G, I);
  cout << "  Done." << endl;

  cout << "Computing Mapper Graph..." << endl;
  vector<double> colors; colors.clear(); vector<int> num; num.clear();
  map<int, vector<int> > MG = build_mapper_graph(M);
  cout << "  Done." << endl;

  char mapp[100] = "mapper.dot";
  ofstream graphic(mapp); graphic << "graph Mapper {" << endl;

  double maxv, minv; maxv = numeric_limits<double>::min(); minv = numeric_limits<double>::max();
  for (vector<double>::iterator iit = colors.begin(); iit != colors.end(); iit++){
    if(*iit > maxv){maxv = *iit;}
    if(minv > *iit){minv = *iit;}
  }

  int k = 0; vector<int> nodes; nodes.clear();
  if(mask > 0){
    for (map<int, vector<int> >::iterator iit = MG.begin(); iit != MG.end(); iit++){
      if(num[k] > mask){
        nodes.push_back(iit->first);
        graphic << iit->first << "[shape=circle fontcolor=black color=black label=\"" << num[k] << "\" style=filled fillcolor=\"" << (maxv-colors[k])/(maxv-minv)*0.6 << ", 1, 1\"]" << endl;
      }
      k++;
    }
  }
  else{
    for (map<int, vector<int> >::iterator iit = MG.begin(); iit != MG.end(); iit++){
      nodes.push_back(iit->first);
      graphic << iit->first << "[shape=circle fontcolor=black color=black label=\"" << num[k] << "\" style=filled fillcolor=\"" << (maxv-colors[k])/(maxv-minv)*0.6 << ", 1, 1\"]" << endl;
      k++;
    }
  }

  for (map<int, vector<int> >::iterator it = MG.begin(); it != MG.end(); it++){
    sort(it->second.begin(), it->second.end()); vector<int>::iterator last = unique(it->second.begin(), it->second.end()); it->second.erase(last, it->second.end());
    for (int j = 0; j < it->second.size(); j++)
      if (it->first > it->second[j])
        if( find(nodes.begin(),nodes.end(),it->first)!=nodes.end() && find(nodes.begin(),nodes.end(),it->second[j])!=nodes.end() )
          graphic << "  " << it->first << " -- " << it->second[j] << " [weight=15];" << endl;
  }
  graphic << "}";

return 0;
}

