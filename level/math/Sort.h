#ifndef _SORT_H_
#define _SORT_H_

#include <algorithm>

template <class Iter, class Comp>
inline void merge_sort(Iter first, Iter last, Comp comp) 
{
	size_t size = last - first;
	if(size < 2) return;
	Iter half = first + size/2;

	merge_sort(first, half, comp);
	merge_sort(half, last, comp);
	merge_merge(first, half, last, comp);
}

template <class Iter, class Comp>
void merge_merge(Iter first, Iter half, Iter last, Comp comp)
{
	for(;first<half;first++)
	{
		if( comp(*half,*first))
		{
			typename std::iterator_traits<Iter>::value_type v;
			std::swap(v,*first);
			std::swap(*first,*half);
			merge_insert(half,last,v,comp);
		}
	}
}

template <class Iter, class Type, class Comp>
void merge_insert(Iter first, Iter last, Type& v, Comp comp)
{
	while(first+1!=last && comp(*(first+1),v))
	{
		std::swap(*first, *(first+1));
		first++;
	}
	swap(*first,v);
}

template <class Iter, class Comp>
inline void insertion_sort(Iter first, Iter last, Comp comp) 
{
	Iter min = first;
	for( Iter i = first + 1; i < last; ++i )
		if ( comp(*i,*min) )
			min = i;
	
	std::iter_swap( first, min );
	while( ++first < last )
		for( Iter j = first; comp(*j,*(j - 1)); --j )
			std::iter_swap( (j - 1), j );
}

template <class Iter, class Comp>
inline void insertion2_sort(Iter first, Iter last, Comp comp)
{
	for (Iter i = first + 1; i < last; ++i)
	{
	    for(Iter j = i; comp(*j,*(j - 1)) && j > first; --j )
	    {
	        std::iter_swap((j - 1), j);
	    }
	}
}



#endif