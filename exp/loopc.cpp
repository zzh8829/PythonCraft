
#include <boost/python.hpp>
using namespace boost::python;
#include <string>
#include <ctime>
using namespace std;

class Looper
{
public:
	Looper(){
		a = "asdfasdfasdfasdf";
	 	n = a.size();
	}
	float loop(){
		clock_t t1 = clock();
		for(int i=0;i!=100;i++)
			for(int j=0;j!=100;j++)
				for(int k=0;k!=100;k++)
				{
					int b = 10;
					int c = b<<4;
					int d = c>>4;
					int asdf = i*j*k;
					int kk = asdf%n;
					char dd = a[kk];
					char dd2 = a[kk];
					char dd3 = a[kk];
					char dd4 = a[kk];
					char dd5 = a[kk];
				}
		return ((float)(clock()-t1))/CLOCKS_PER_SEC;
	}

	string a;
	int n;
};

BOOST_PYTHON_MODULE(loopc)
{
	class_<Looper>("Looper")
		.def("loop",&Looper::loop);
}