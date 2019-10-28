#include <cstdio>
#include <vector>
#include <cstring>
#include <iostream>
#include <algorithm>

using namespace std;

const int max_m = 20000;
const int max_n = 500;
const long long inf = (long long) 1e18;

struct edge
{
	int toV, next, c, f;
};

int freeE, start[max_n], n, q[max_n], d[max_n], s, t, ptr[max_n];
edge r[max_m];

void simple_add(int u, int v, int c)
{
	r[freeE].toV = v, r[freeE].next = start[u], r[freeE].c = c, r[freeE].f = 0, start[u] = freeE, freeE++;
}

void add(int u, int v, int c)
{
	simple_add(u, v, c), simple_add(v, u, 0);
}

void bfs()
{
	int qh = 0, qe = 1;
	for (int i = 0; i < n; ++i)
		d[i] = n + 1;
	q[0] = s, d[s] = 0;
	while (qh < qe)
	{
		int u = q[qh++];
		for (int j = start[u]; j != -1; j = r[j].next)
			if ((d[r[j].toV] > d[u] + 1) && (r[j].c - r[j].f > 0))
				d[r[j].toV] = d[u] + 1, q[qe++] = r[j].toV;
	}
	for (int i = 0; i < n; ++i)
		ptr[i] = start[i];
}

long long dfs(int v, long long mx)
{
	if ((v == t) || (mx == 0))
		return mx;
	long long res = 0;
	for ( ; (mx > 0) && (ptr[v] != -1); ptr[v] = r[ptr[v]].next)
	{
		if (d[r[ptr[v]].toV] != d[v] + 1) 
			continue;
		long long tmp = dfs(r[ptr[v]].toV, min(mx, 0ll + r[ptr[v]].c - r[ptr[v]].f));
		if (tmp > 0)
		{
			r[ptr[v]].f += tmp;
			r[ptr[v] ^ 1].f -= tmp;
			mx -= tmp;
			res += tmp;
			if (mx == 0)
				return res;
		}
	}
	return res;
}

vector < vector <int> > result;
vector < int > current;

bool decompose(int s, long long f)
{
	cerr << s << " " << f << endl;
	if (s == t)
	{
		current.push_back((int) f);
		result.push_back(current);
		current.pop_back();
		return true;
	}
	bool res = false;
	for (int j = start[s]; j != -1; j = r[j].next)
	{
		current.push_back(j / 2 + 1);
		long long to_push = min(r[j].f + 0ll, f);
		if ((to_push > 0) && (decompose(r[j].toV, to_push)))
		{
			res = true;
			r[j].f -= to_push;
			f -= to_push;
		}
		current.pop_back();
	}
	return res;
}

int main()
{
	freopen("decomposition.in", "r", stdin);
	freopen("decomposition.out", "w", stdout);
	int m, u, v, c;
	scanf("%d%d", &n, &m);
	s = 0, t = n - 1;
	memset(start, -1, sizeof(start));
	for (int i = 0; i < m; ++i)
	{
		scanf("%d%d%d", &u, &v, &c);
		u--, v--;
		add(u, v, c);
	}
	long long f = 0;
	for (int i = 0; i < n; ++i)
	{
		bfs();
		f += dfs(s, inf);
	}
	for( ; decompose(s, f); );
	printf("%d\n", result.size());
	for (int i = 0; i < result.size(); ++i)
	{
		printf("%d %d", result[i].back(), result[i].size() - 1);
		for (int j = 0; j < result[i].size() - 1; ++j)
			printf(" %d", result[i][j]);
		printf("\n");
	}
	return 0;
}