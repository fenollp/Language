#include <iostream>

using namespace std;

int ∑† ( int nb )
{
	int somme_aliquotes = 0;
	int aliquote = 0;

	for ( int i = 0; i < nb; i++ )
		if ( aliquote = (nb % i) == 0 )
			somme_aliquotes += aliquote;

	return somme_aliquotes;
}

int main()
{
    cout << "Hello world!" << endl <<
    ∑†(2) << endl;

    return EXIT_SUCCESS;
}
