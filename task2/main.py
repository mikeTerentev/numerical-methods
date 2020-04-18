import numpy as np
import plotly.graph_objects as go


def fixed_point_iteration(f, x0, iter_num):
    """
    Calculates first iter_num iterations of f(x)

    Parameters
    ----------
    f: function (float -> float)
        Function to explore.
    iter_num : int
        Number of iterations.
    r : float
        Parameter in equation.

    Returns list of iteration points

    """
    xi = x0
    points = [xi]
    for i in range(iter_num):
        xi = f(xi)
        points.append(xi)
    return np.asarray(points)


def plot_seq(rs, iterations, x0=np.random.rand()):
    fig = go.Figure()
    for r in rs:
        fig.add_trace(go.Scatter(
            x=np.arange(iterations),
            y=fixed_point_iteration(lambda x: r * x * (1 - x), x0, iterations),
            mode="lines",
            name=f"r={r}"
        ))
    fig.update_traces(marker={
        "size": 1,
        "line": {
            "width": 1
        }
    })
    fig.update_layout(
        autosize=False,
        width=1080 * 16 // 9,
        height=1080
    )
    fig.update_xaxes(title_text="i",
                     title_font={"size": 25})
    fig.update_yaxes(title_text="x_i",
                     title_font={"size": 25})
    fig.write_image(f"images/iter.png")


def plot_trajectory(r, iter_num, x0, fig):
    f = lambda x: r * x * (1 - x)
    points = fixed_point_iteration(f, x0, iter_num)
    fig.add_trace(go.Scatter(
        x=np.linspace(0, 1, 100),
        y=f(np.linspace(0, 1, 100))
    ))
    fig.add_trace(
        go.Scatter(x=[points[(t + 1) // 2] for t in range(2 * len(points) - 3)],
                   y=[points[1 + t // 2] for t in range(2 * len(points) - 3)],
                   mode="lines+markers",
                   opacity=0.8,
                   name=f"r = {'{:.2f}'.format(r)}, x0 = {'{:.2f}'.format(x0)}"))


def plot_id(fig):
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines"))


def explore_segment(start, stop, iterations=50, step=0.1):
    fig = go.Figure()
    plot_id(fig)
    for r in np.arange(start, stop, step):
        plot_trajectory(r, iterations, np.random.rand(), fig)
        r += step

    fig.update_traces(marker={
        "size": 1,
        "line": {
            "width": 1
        }
    })
    fig.update_layout(
        autosize=False,
        width=1080,
        height=1080
    )
    fig.update_xaxes(title_text="x",
                     title_font={"size": 25})
    fig.update_yaxes(title_text="p * x * (1 - x)",
                     title_font={"size": 25})
    fig.write_image(f"images/{'{:.2f}'.format(start)}-{'{:.2f}'.format(stop)}.png")


def partial_limits(r, n):
    f = lambda x: r * x * (1 - x)
    eps = 0.00001
    converged = [False for i in range(n)]
    terms = np.ones(n)
    terms[0] = (np.random.rand() + 0.5) / 2
    for i in range(1, 10000000):
        g = f(terms[(i - 1) % n])
        if abs(g - terms[i % n]) < eps:
            converged[i % n] = True
        terms[i % n] = g
        if i % n == 0 and np.all(converged):
            break
    if not np.all(converged):
        return None
    return terms


def bifourin():
    xs = []
    ys = []
    r_inf = np.float(3.5699456)
    delta = np.float(4.66920116)

    def fract(r):
        if r < 3:
            return 0
        i = 1
        denom = delta
        while r > r_inf - 1.0 / denom:
            denom *= delta
            i += 1
            if i > 11:
                return
        return i

    for r in np.linspace(0, r_inf, 10000):
        size = fract(r)
        if size is None:
            break
        res = partial_limits(r, 2 ** size)
        if res is None:
            break
        xs.extend([r for i in range(2 ** size)])
        ys.extend(res)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers"))
    fig.update_traces(marker={
        "size": 1,
        "line": {
            "width": 1
        }
    })
    fig.update_layout(
        autosize=False,
        width=1080 * 16 // 9,
        height=1080
    )
    fig.update_xaxes(title_text="p",
                     title_font={"size": 25})
    fig.update_yaxes(title_text="partial limits",
                     title_font={"size": 25})
    fig.write_image(f"images/bifour.png")


def feigenbaum(index):
    r_inf = np.float(3.5699456)
    delta = np.float(4.66920116)
    return r_inf - np.divide(np.float(1.0), np.power(delta, index))


borders = [feigenbaum(i) for i in range(1, 4)]

np.random.seed(None)

explore_segment(0.1, 1, 50, step=0.4)
explore_segment(1.2, 2, 50, step=0.3)
explore_segment(2.2, 3, 50, step=0.3)
explore_segment(3.1, 3.3, 200)
for i in range(2):
    explore_segment((3 * borders[i] + borders[i + 1]) / 4, borders[i+1], 200, step=(borders[i + 1] - borders[i]) / 2)
explore_segment(3.75, 3.82, 200, step=0.05)
explore_segment(3.8, 3.87, 200, step=0.05)
explore_segment(3.85, 3.92, 200, step=0.05)
explore_segment(3.9, 3.97, 200, step=0.05)
bifourin()
plot_seq(np.append(np.arange(0.75, 4, 0.5), np.array([3.53])), 100)
