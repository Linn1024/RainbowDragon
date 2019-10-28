import java.io.*;
import java.util.*;
import java.math.*;

public class decomposition_ab implements Runnable {

    final int MAXN = 500;
    final int MAXM = 10000;
    final long MAXC = (long)(1e14);
    
    private void solve() throws IOException {
        int n = in.nextInt();
        if (n < 2 || n > MAXN) throw new Error();
        int m = in.nextInt();
        if (m < 1 || m > MAXM) throw new Error();
        
        g = new ArrayList[n];
        for (int i = 0; i < n; ++i) {
            g[i] = new ArrayList<Edge>();
        }
        
        for (int i = 0; i < m; ++i) {
            int a = in.nextInt() - 1;
            int b = in.nextInt() - 1;
            if (a < 0 || a >= n) throw new Error();
            if (b < 0 || b >= n) throw new Error();
            long c = in.nextLong();
            if (c < 0 || c > MAXC) throw new Error();
            addEdge(a, b, i, c);
        }
        
        cl = new int[n];
        col = 1;
        long mask = Long.highestOneBit(MAXC) << 1;
        while ((mask & 1) == 0) {
            mask |= mask >> 1;
            ++col;
            while (dfs(0, n - 1, Long.MAX_VALUE, mask) > 0) {
                ++col;
            }
        }
        
        ArrayList<Path> ans = new ArrayList<Path>();
        
        while (true) {
            ++col;
            Path tp = dfsCut(0, n - 1, Long.MAX_VALUE);
            if (tp != null) {
                Collections.reverse(tp.edges);
                ans.add(tp);
            } else {
                break;
            }
        }
        
        out.println(ans.size());
        for (Path p : ans) {
            out.print(p.fl + " " + p.edges.size());
            for (int i : p.edges) {
                out.print(" " + (i + 1));
            }
            out.println();
        }
    }

    Path dfsCut(int i, int t, long mf) {
        if (i == t) {
            return new Path(mf);
        }
        cl[i] = col;
        for (Edge e : g[i]) {
            if (e.f > 0 && cl[e.j] != col) {
                Path tp = dfsCut(e.j, t, Math.min(e.f, mf));
                if (tp != null) {
                    e.f -= tp.fl;
                    tp.edges.add(e.num);
                    return tp;
                }
            }
        }
        return null;
    }
    
    class Path {
        long fl;
        ArrayList<Integer> edges;
        
        public Path(long fl) {
            this.fl = fl;
            edges = new ArrayList<Integer>();
        }
    }
    
    ArrayList<Edge>[] g;
    int[] cl;
    int col;
    
    long dfs(int i, int t, long min, long mask) {
        if (i == t) return min;
        cl[i] = col;
        for (Edge e : g[i]) {
            if (cl[e.j] != col && (e.c & mask) > 0) {
                long fl = dfs(e.j, t, Math.min(e.c & mask, min), mask);
                if (fl != 0) {
                    e.c -= fl;
                    e.f += fl;
                    e.r.c += fl;
                    e.r.f -= fl;
                    return fl;
                }
            }
        }
        return 0;
    }
    
    void addEdge(int i, int j, int num, long c) {
        Edge e = new Edge(j, c, num);
        Edge re = new Edge(i, 0, num);
        e.r = re;
        re.r = e;
        g[i].add(e);
        g[j].add(re);
    }
    
    class Edge {
        int j, num;
        long c, f;
        Edge r;
        
        public Edge(int j, long c, int num) {
            this.j = j;
            this.c = c;
            this.num = num;
        }
    }
    

    final String FILE_NAME = "decomposition";

    SimpleScanner in;
    PrintWriter out;

    @Override
    public void run() {
        try {
            in = new SimpleScanner(new FileReader(FILE_NAME + ".in"));
            out = new PrintWriter(FILE_NAME + ".out");
            solve();
            out.close();
        } catch (Throwable e) {
            e.printStackTrace();
            System.exit(-1);
        }
    }

    public static void main(String[] args) {
        new Thread(new decomposition_ab()).start();
    }

    class SimpleScanner extends BufferedReader {

        private StringTokenizer st;
        private boolean eof;

        public SimpleScanner(Reader a) {
            super(a);
        }

        String next() {
            while (st == null || !st.hasMoreElements()) {
                try {
                    st = new StringTokenizer(readLine());
                } catch (Exception e) {
                    eof = true;
                    return "";
                }
            }
            return st.nextToken();
        }

        boolean seekEof() {
            String s = next();
            if ("".equals(s) && eof)
                return true;
            st = new StringTokenizer(s + " " + st.toString());
            return false;
        }

        private String cnv(String s) {
            if (s.length() == 0)
                return "0";
            return s;
        }

        int nextInt() {
            return Integer.parseInt(cnv(next()));
        }

        double nextDouble() {
            return Double.parseDouble(cnv(next()));
        }

        long nextLong() {
            return Long.parseLong(cnv(next()));
        }
    }
}