# solar_app — Two-Tier Solar Analytics with Containerised Continuous Deployment

Two independent Streamlit applications — a **free tier** and a **paid tier** — each
containerised separately and deployed to Heroku through its own GitHub Actions workflow.

The interesting part of this repository is the **deployment pipeline**, not the size of
the apps: two independently built and released services out of one monorepo, where a
change to one tier does not rebuild or redeploy the other.

---

## Repository layout

```
solar_app/
├── dev_apps/                    # free tier
│   ├── app.py                   # PV IV-curve simulator
│   ├── Dockerfile               # python:3.9-slim
│   └── requirements.txt         # streamlit, matplotlib, numpy
├── paid_apps/                   # paid tier
│   ├── app.py                   # savings-vs-efficiency projection
│   ├── Dockerfile               # python:3.9-slim
│   └── requirements.txt         # streamlit, plotly, numpy
└── .github/workflows/
    ├── deploy-dev.yml           # triggers only on dev_apps/**
    └── deploy-paid.yml          # triggers only on paid_apps/**
```

---

## The applications

### Free tier — Solar PV IV Curve Simulator (`dev_apps/`)

Plots the current–voltage characteristic of a photovoltaic cell from the **single-diode
model**, with irradiance and cell temperature as interactive inputs.

$$I = I_{ph} - I_0\left(e^{V/V_t} - 1\right), \qquad V_t = \frac{nkT}{q}$$

- **Irradiance** (100–1000 W/m²) scales the photocurrent $I_{ph}$ linearly.
- **Temperature** (−10 to 100 °C) enters in two places: it raises $V_t$ through $T$ in
  kelvin, and it increases the reverse saturation current $I_0$ exponentially — which is
  why raising the temperature lowers the open-circuit voltage while barely changing the
  short-circuit current.
- Ideality factor `n = 1.3`, $I_0 = 10^{-10}$ A, $I_{ph} = 5$ A at 1000 W/m².

Rendered with Matplotlib.

### Paid tier — Savings Projection (`paid_apps/`)

An interactive Plotly chart of projected savings against panel efficiency, with the
user's selected efficiency annotated on the curve.

Inputs are wrapped in a `st.form` block so the model recomputes **once on submit**
rather than on every widget interaction — Streamlit reruns the whole script on any
widget change by default, which is wasteful for anything more expensive than a slider.

> **Note:** the savings curve is illustrative. It uses a fixed baseline and a fitted
> exponent to shape the curve; it is not calibrated against tariff or generation data.

---

## Deployment pipeline

Both tiers deploy to Heroku via the **container registry**, driven by GitHub Actions.

**Path filtering.** Each workflow only fires for its own directory:

```yaml
on:
  push:
    paths:
      - 'dev_apps/**'
      - '.github/workflows/deploy-dev.yml'
    branches: [ main ]
```

So editing the free tier never triggers a paid-tier rebuild, and vice versa. Both
workflows also watch their own file, so changing a workflow redeploys the tier it owns.

**Non-interactive authentication.** The runner has no TTY, so the Heroku CLI is
authenticated by writing `~/.netrc` directly from a repository secret:

```yaml
- name: Authenticate Heroku CLI
  run: |
    echo "machine api.heroku.com
      login _
      password ${{ secrets.HEROKU_API_KEY }}
    machine git.heroku.com
      login _
      password ${{ secrets.HEROKU_API_KEY }}" > ~/.netrc
```

**Images.** Both Dockerfiles build on `python:3.9-slim` and install with
`pip install --no-cache-dir`, keeping the layers small. The container binds Streamlit to
the port Heroku injects at runtime:

```dockerfile
CMD streamlit run app.py --server.port=$PORT --server.enableCORS=false
```

---

## Running locally

```bash
# free tier
cd dev_apps
pip install -r requirements.txt
streamlit run app.py

# or with Docker
docker build -t solar-dev .
docker run -p 8501:8501 -e PORT=8501 solar-dev
```

Swap `dev_apps` for `paid_apps` to run the paid tier.

---

## Required secret

| Secret | Used by | Purpose |
|---|---|---|
| `HEROKU_API_KEY` | both workflows | Heroku CLI and container-registry authentication |

Set the Heroku app names in the workflow files to match your own before deploying.
