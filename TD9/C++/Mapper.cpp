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

class Point{

  public:

    int ID;
    double func;
    vector<double> coord;

    Point(){}
    Point(const int & _ID){ID = _ID;} // constructor 1
    Point(const int & _ID, const vector<double> & _coord){ID = _ID; coord = _coord;} // constructor 2
    bool operator<(const Point & p) const {if(this->func != p.func){return this->func < p.func;}else{return this->ID < p.ID;}} // comparator
    bool operator==(const Point & p) const {return this->ID == p.ID;}
    double EuclideanDistance(const Point & p) const {
      assert (this->coord.size() == p.coord.size());
      double x = 0; int dim = p.coord.size(); for (int i = 0; i < dim; i++){x+=(this->coord[i]-p.coord[i])*(this->coord[i]-p.coord[i]);}
      return sqrt(x);
    };

};

bool comp(const pair<double, double> & I1, const pair<double, double> & I2){return I1.second < I2.second;}

class Cover{

  public:

    int res;
    vector<pair<double, double> > intervals;

    Cover(){}
    Cover(const double & minf, const double & maxf, const double & resolution, const double & gain){
      double incr = (maxf-minf)/resolution; double x = minf; double alpha = (incr*gain)/(2*(1-gain)); double y = min(x+incr+2*alpha, maxf);
      while(y != maxf){
        pair<double, double> inter(x,y); intervals.push_back(inter);
        x = y-2*alpha; y = min(x+incr+2*alpha, maxf);
      }
      pair<double, double> inter(x,y); intervals.push_back(inter); res = intervals.size();
    }

    Cover(char* const & name){
      ifstream input(name); intervals.clear();
      if(input){
        string line;
        while(getline(input,line)){
          pair<double, double> inter; double x = numeric_limits<double>::max();
          stringstream stream(line);
          stream >> x; inter.first = x; stream >> x; inter.second = x;
          if(x != numeric_limits<double>::max()){assert (inter.first <= inter.second); intervals.push_back(inter);}
        }
        res = intervals.size();
      }
      else{cout << "  Failed to read file " << name << endl;}
    }

    void sort_covering(){sort(this->intervals.begin(),this->intervals.end(), comp);}
};

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

Graph build_neighborhood_graph_from_file(const Cloud & C, char* const & name){

  int nb = C.size(); Graph G; G.clear(); vector<Point> adj; adj.clear();
  for(int i = 0; i < nb; i++)
    G.insert(pair<Point, vector<Point> >(C[i],adj));
  ifstream input(name);
  if(input){
    string line; int v1, v2; int k = 0;
    while(getline(input,line)){
      int x = numeric_limits<int>::max();
      stringstream stream(line);
      stream >> x; v1 = x; stream >> x; v2 = x;
      if(x != numeric_limits<int>::max()){G[C[v1]].push_back(C[v2]);G[C[v2]].push_back(C[v1]); k++;}
    }
    cout << "  " << 100*((double) k)/((double) nb*(nb-1)/2) << "% of pairs selected." << endl;
  }
  else{cout << "Failed to read file " << name << endl; return G;}

}

Graph build_neighborhood_graph_from_scratch(const Cloud & C, const double & delta, char* const & name){

  ofstream output(name);
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
        output << C[i].ID << " " << C[j].ID << endl;
      }
    }
  }
  cout << 100*((double) k)/((double) nb*(nb-1)/2) << "% of pairs selected." << endl;
  return G;
}

void dfs(Graph & G, const Point & p, vector<Point> & cc, map<Point,bool> & visit){
  cc.push_back(p);
  visit[p] = true; int neighb = G[p].size(); // Penser a mettre un assert : verifier que p est bien une cle de G
  for (int i = 0; i < neighb; i++)
    if (  visit.find(G[p][i]) != visit.end() )
      if(  !(visit[G[p][i]])  )
        dfs(G,G[p][i],cc,visit);
}

ConnectedComp count_cc(Graph & G, int & id){
  map<Point,bool> visit;
  for(Graph::iterator it = G.begin(); it != G.end(); it++)
    visit.insert(pair<Point,bool>(it->first, false));
  ConnectedComp CC; CC.clear();
  if (!(G.empty())){
    for(Graph::iterator it = G.begin(); it != G.end(); it++){
      if (  !(visit[it->first])  ){
        vector<Point> cc; cc.clear();
        dfs(G,it->first,cc,visit);
        CC.insert(pair<int, vector<Point> >(id,cc)); id++;
      }
    }
  }
  return CC;
}

vector<ConnectedComp> MapperElts(Graph & G, const Cover & I){

  Graph::iterator pos = G.begin();
  vector<ConnectedComp> mapper_elts;
  mapper_elts.clear();
  int id = 0;

  for(int i = 0; i < I.res; i++){

    pair<double, double> inter1 = I.intervals[i];
    Graph g1, g2; Graph::iterator tmp = pos;
    if(i != I.res-1){
      g1.clear(); g2.clear();
      pair<double, double> inter2 = I.intervals[i+1];
      while(tmp->first.func < inter2.first && tmp != G.end()){g1.insert(pair<Point,vector<Point> >(tmp->first,tmp->second)); tmp++;}
      pos = tmp;
      while(tmp->first.func < inter1.second && tmp != G.end()){
        g1.insert(pair<Point,vector<Point> >(tmp->first,tmp->second));
        g2.insert(pair<Point,vector<Point> >(tmp->first,tmp->second));
        tmp++;
      }
      ConnectedComp CC1 = count_cc(g1,id); mapper_elts.push_back(CC1); //cout << i << ": added " << CC1.size() << " proper nodes" << endl;
      ConnectedComp CC2 = count_cc(g2,id); mapper_elts.push_back(CC2); //cout << i << ": added " << CC2.size() << " intersections" << endl;
    }
    else{
      g1.clear();
      while(tmp != G.end()){g1.insert(pair<Point,vector<Point> >(tmp->first,tmp->second)); tmp++;}
      ConnectedComp CC1 = count_cc(g1,id); mapper_elts.push_back(CC1); //cout << i << ": added " << CC1.size() << " proper nodes" << endl;
    }

  }

  return mapper_elts;
}


map<int, vector<int> > build_mapper_graph(vector<ConnectedComp> & M, vector<double> & colors, vector<int> & num){
  map<int, vector<int> > MG; MG.clear(); vector<int> adj;
  int nb_elts = M.size(); adj.clear();
  for (int i = 0; i < nb_elts; i+=2){
    for (ConnectedComp::iterator it = M[i].begin(); it != M[i].end(); it++){
      int p = it->first; MG.insert(pair<int, vector<int> >(p,adj)); int inside_nb = it->second.size(); double c = 0;
      for (int j = 0; j < inside_nb; j++)
        c+=it->second[j].func;
      c/=inside_nb; colors.push_back(c); num.push_back(inside_nb);
    }
  }
  for (int i = 1; i < nb_elts; i+=2){
    if (!M[i].empty()){
      for (ConnectedComp::iterator it = M[i].begin(); it != M[i].end(); it++){
        Point p = it->second[0]; int v1 = -1; int v2 = -1;
        for (ConnectedComp::iterator iit = M[i-1].begin(); iit != M[i-1].end(); iit++)
          if(  find(iit->second.begin(), iit->second.end(), p) != iit->second.end()  ){v1 = iit->first; break;}
        for (ConnectedComp::iterator iit = M[i+1].begin(); iit != M[i+1].end(); iit++)
          if(  find(iit->second.begin(), iit->second.end(), p) != iit->second.end()  ){v2 = iit->first; break;}
        if(v1 != -1 && v2 != -1){MG[v1].push_back(v2); MG[v2].push_back(v1);}
      }
    }
  }
  return MG;
}

vector<pair<int,int> > check_intersection_crossing(const vector<ConnectedComp> & M, Graph & G){
  int nb_elts = M.size(); vector<pair<int,int> > pairs; pairs.clear();
  for (int i = 0; i < nb_elts-1; i+=2){
    ConnectedComp CC1 = M[i]; ConnectedComp CC2 = M[i+2];
    for(ConnectedComp::iterator it = CC1.begin(); it != CC1.end(); it++){
      int cc1_nb = it->second.size();
      for(ConnectedComp::iterator iit = CC2.begin(); iit != CC2.end(); iit++){
        int cc2_nb = iit->second.size(); int i = 0; bool point_in_inter = false; int count_interval_cross = 0;
        //cout << "  Checking nodes " << it->first << " and " << iit->first << "..." << endl;
        while(i < cc1_nb && !point_in_inter){
          Point p1 = it->second[i]; int j = 0;
          while(j < cc2_nb && !point_in_inter){
            Point p2 = iit->second[j];
            if(p1 == p2){point_in_inter = true;}
            if(  find(G[p1].begin(),G[p1].end(),p2)!=G[p1].end()  ){count_interval_cross++;}
            j++;
          }
          i++;
        }
        if(!point_in_inter && count_interval_cross > 0){
          cout << "  Warning: nodes " << it->first << " and " << iit->first << " separated whereas they should not: " << count_interval_cross << " intersection crossings" << endl;
          pairs.push_back(pair<int,int>(it->first,iit->first));
        }
      }
    }
  }
  return pairs;
}

int main(int argc, char** argv){

  if(argc <= 9){cout << "Usage: <cloud_file> <function:/coordinate:> <func_file/number> <graph:/parameter:> <graph_file/delta> <mask:> <number> <covering:/uniform:> <covering_file/resolution> <gain>" << endl; return 0;}
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
  /*
  for (int i = 0; i < C.size(); i++)
    cout << C[i].ID << " " << C[i].coord[0] << " " << C[i].coord[1] << " " << C[i].coord[2] << " " << C[i].func << endl;
  */
  if (strcmp(graph, "graph:") == 0){
    char* const graph_name = argv[5];
    cout << "Reading neighborhood graph from file " << graph_name << "..." << endl;
    G = build_neighborhood_graph_from_file(C,graph_name);
  }
  else{
    double delta = atof(argv[5]);
    char name1[100]; sprintf(name1, "%s_NG_%g", cloud, delta); char* const name2 = name1;
    cout << "Computing neighborhood graph with delta parameter = " << delta << "..." << endl;
    G = build_neighborhood_graph_from_scratch(C,delta,name2);
  }
  cout << "  Done." << endl;

  cout << "Sorting cloud..." << endl;
  sort(C.begin(),C.end());
  cout << "  Done." << endl;
  /*
  for (int i = 0; i < C.size(); i++)
    if(C[i].func <= -1.1)
      cout << C[i].ID << " " << C[i].coord[0] << " " << C[i].coord[1] << " " << C[i].coord[2] << " " << C[i].func << endl;
  */
  if(strcmp(covering,"covering:") == 0){
    char* const cover = argv[9];
    cout << "Reading user-defined covering from file " << cover << "..." << endl;
    I = Cover(cover); I.sort_covering();
    assert (I.intervals[0].first <= C.begin()->func && I.intervals[I.intervals.size()-1].second >= (C.end()-1)->func);
  }
  else{
    double resolution = atoi(argv[9]);
    double gain = atof(argv[10]); assert (gain >= 0);
    cout << "Computing uniform covering with resolution " << resolution << " and gain " << gain << "..." << endl;
    I = Cover(C.begin()->func, (C.end()-1)->func, resolution, gain);
  }
  cout << "  Done." << endl;
  /*
  for (int i = 0; i < I.res; i++)
    cout << I.intervals[i].first << " " << I.intervals[i].second << endl;
  */
  cout << "Computing Mapper Elements..." << endl;
  M = MapperElts(G,I);
  cout << "  Done." << endl;
  /*
  for (int i = 0; i < M.size(); i++){
    if (i % 2 == 0)
      cout << "proper interval " << i/2 << endl;
    else
      cout << "intersection interval " << (i-1)/2 << endl;
    if(!(M[i].empty())){
      for(ConnectedComp::iterator it = M[i].begin(); it != M[i].end(); it++){
        cout << "  cc " << (it->first) << " of size "; cout << (it->second).size() << ": ";
        for(int j = 0; j < (it->second).size(); j++)
          cout << (it->second)[j].ID << ", ";
        cout << endl;
      }
    }
    else{cout << "  empty" << endl;}
  }
  */
  cout << "Computing Mapper Graph..." << endl;
  vector<double> colors; colors.clear(); vector<int> num; num.clear();
  map<int, vector<int> > MG = build_mapper_graph(M,colors,num);
  cout << "  Done." << endl;
  /*
  cout << endl;
  cout << "Mapper graph has nodes: ";
  for (map<int, vector<int> >::iterator it = MG.begin(); it != MG.end(); it++)
    cout << it->first << " ";
  cout << endl;
  for (map<int, vector<int> >::iterator it = MG.begin(); it != MG.end(); it++){
    cout << "node " << it->first << " have neighbors: ";
    for (int j = 0; j < it->second.size(); j++)
      cout << it->second[j] << " ";
    cout << endl;
  }
  */

  //cout << "Checking intersection crossings..." << endl;
  //vector<pair<int,int> > error_pairs = check_intersection_crossing(M,G);
  //cout << "Done." << endl;

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
        graphic << iit->first << "[shape=circle fontcolor=black color=black label=\"" << iit->first << ":" << num[k] << "\" style=filled fillcolor=\"" << (maxv-colors[k])/(maxv-minv)*0.6 << ", 1, 1\"]" << endl;
      }
      k++;
    }
  }
  else{
    for (map<int, vector<int> >::iterator iit = MG.begin(); iit != MG.end(); iit++){
      nodes.push_back(iit->first);
      graphic << iit->first << "[shape=circle fontcolor=black color=black label=\"" << iit->first << ":" << num[k] << "\" style=filled fillcolor=\"" << (maxv-colors[k])/(maxv-minv)*0.6 << ", 1, 1\"]" << endl;
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
  /*
  if (error_pairs.size() > 0)
    for (vector<pair<int,int> >::iterator it = error_pairs.begin(); it != error_pairs.end(); it++)
      if( find(nodes.begin(),nodes.end(),it->first)!=nodes.end() && find(nodes.begin(),nodes.end(),it->second)!=nodes.end() )
        graphic << "  " << it->first << " -- " << it->second << " [weight=15];" << endl;
  */
  graphic << "}";

return 0;
}
