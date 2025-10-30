# simulate_3i_atlas.py

"""
Simulação simples (2-corpos) da passagem do 3I/ATLAS (C/2025 N1) pelo Sistema Solar.
Gera:
  - 3I_ATLAS_distancia_vs_tempo.png
  - 3I_ATLAS_trajetoria_perifocal.png
e exibe os gráficos na tela.

Dependências: numpy, matplotlib (instale com: pip install numpy matplotlib)
Uso:
  python simulate_3i_atlas.py
  # ou com opções:
  python simulate_3i_atlas.py --tmin -200 --tmax 200 --points 2001 --out .
"""

import math
import argparse
from datetime import datetime, timezone, timedelta

import numpy as np
import matplotlib.pyplot as plt


def solve_H(Mh: float, e: float, tol: float = 1e-12, maxit: int = 100) -> float:
    """
    Resolve a equação de Kepler hiperbólica:
      Mh = e*sinh(H) - H
    via Newton-Raphson.
    """
    if abs(Mh) > 1.0:
        H = np.arcsinh(Mh / e)
    else:
        H = Mh / (e - 1.0)
    for _ in range(maxit):
        s = math.sinh(H)
        c = math.cosh(H)
        f = e * s - H - Mh
        fp = e * c - 1.0
        dH = -f / fp
        H += dH
        if abs(dH) < tol:
            break
    return H


def main():
    ap = argparse.ArgumentParser(description="Simulação 2-corpos do 3I/ATLAS")
    ap.add_argument("--tmin", type=float, default=-200.0, help="Dias antes do periélio")
    ap.add_argument("--tmax", type=float, default=200.0, help="Dias após o periélio")
    ap.add_argument("--points", type=int, default=2001, help="Número de amostras no tempo")
    ap.add_argument("--out", type=str, default=".", help="Diretório de saída dos PNGs")
    args = ap.parse_args()

    # ==============================
    # Constantes e elementos orbitais
    # ==============================
    k_gauss = 0.01720209895  # [AU^(3/2)/dia]
    mu = k_gauss ** 2        # GM do Sol [AU^3/dia^2]

    # Elementos nominais (consistentes com resumos públicos)
    q = 1.3565        # distância de periélio [AU]
    a = -0.26549      # semi-eixo maior [AU] (hipérbole => negativo)
    e = 1.0 + (q / abs(a))  # ~6.11

    # Época do periélio (UTC)
    T_peri = datetime(2025, 10, 29, 11, 15, 0, tzinfo=timezone.utc)

    # Malha temporal
    t_days = np.linspace(args.tmin, args.tmax, args.points)

    # Escala característica hiperbólica
    tau = math.sqrt((abs(a) ** 3) / mu)

    # Resolver Kepler hiperbólico para cada instante
    Mh = t_days / tau
    H = np.array([solve_H(float(m), e) for m in Mh])

    # Distância heliocêntrica r(t) = a * (e*cosh(H) - 1), positivo no final
    r = np.abs(a * (e * np.cosh(H) - 1.0))

    # Coordenadas perifocais (ilustração do traço orbital no plano da eclíptica)
    coshH = np.cosh(H)
    sinhH = np.sinh(H)
    x_peri = a * (e - coshH)
    y_peri = a * math.sqrt(e ** 2 - 1.0) * sinhH

    times = [T_peri + timedelta(days=float(dt)) for dt in t_days]

    # ---------- Gráfico 1: Distância vs. Tempo ----------
    plt.figure(figsize=(9, 5))
    plt.plot(times, r, lw=2)
    plt.axvline(T_peri, linestyle='--')
    plt.scatter([T_peri], [q], zorder=5)
    plt.title("3I/ATLAS — Distância Heliocêntrica vs. Tempo (modelo 2-corpos)")
    plt.xlabel("Tempo (UTC)")
    plt.ylabel("Distância ao Sol [UA]")
    plt.grid(True)
    plt.annotate(
        f"Periélio\n{T_peri.strftime('%Y-%m-%d %H:%M UTC')}\nq ≈ {q:.3f} UA",
        xy=(T_peri, q),
        xytext=(times[len(times) // 2], q + 0.4),
        arrowprops=dict(arrowstyle="->"),
    )
    plt.tight_layout()
    out1 = f"{args.out.rstrip('/')}/3I_ATLAS_distancia_vs_tempo.png"
    plt.savefig(out1, dpi=160)

    # ---------- Gráfico 2: Trajetória no plano perifocal ----------
    theta = np.linspace(0.0, 2.0 * np.pi, 400)
    circ1x, circ1y = np.cos(theta), np.sin(theta)

    plt.figure(figsize=(6, 6))
    plt.plot(x_peri, y_peri, lw=2, label="Órbita (perifocal)")
    plt.plot(circ1x, circ1y, linestyle="--", alpha=0.6, label="1 UA")
    plt.plot(1.52 * circ1x, 1.52 * circ1y, linestyle=":", alpha=0.6, label="~Órbita de Marte")
    plt.scatter([0], [0], s=80, marker="o", label="Sol")
    xq = a * (e - 1.0)
    yq = 0.0
    plt.scatter([xq], [yq], s=50, label="Periélio")
    plt.axis("equal")
    plt.xlabel("x [UA]")
    plt.ylabel("y [UA]")
    plt.title("3I/ATLAS — Trajetória no plano perifocal (ilustração)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    out2 = f"{args.out.rstrip('/')}/3I_ATLAS_trajetoria_perifocal.png"
    plt.savefig(out2, dpi=160)

    # Mostrar os gráficos na tela
    print("Arquivos salvos:")
    print(" -", out1)
    print(" -", out2)
    plt.show()


if __name__ == "__main__":
    main()
