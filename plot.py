import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import LogLocator

_sm_fermions = {
    "tops": {
        "mass": 172.76,
        "charge": 2 / 3,
        "baryon_number": 1 / 3,
        "lepton_number": 0,
    },
    "bottoms": {
        "mass": 4.18,
        "charge": -1 / 3,
        "baryon_number": 1 / 3,
        "lepton_number": 0,
    },
    "taus": {
        "mass": 1.77686,
        "charge": -1,
        "baryon_number": 0,
        "lepton_number": 1,
    },
    "charms": {
        "mass": 1.27,
        "charge": 2 / 3,
        "baryon_number": 1 / 3,
        "lepton_number": 0,
    },
    "stranges": {
        "mass": 0.096,
        "charge": -1 / 3,
        "baryon_number": 1 / 3,
        "lepton_number": 0,
    },
    "muons": {
        "mass": 0.105658,
        "charge": -1,
        "baryon_number": 0,
        "lepton_number": 1,
    },
    "ups": {
        "mass": 0.0023,
        "charge": 2 / 3,
        "baryon_number": 1 / 3,
        "lepton_number": 0,
    },
    "downs": {
        "mass": 0.0048,
        "charge": -1 / 3,
        "baryon_number": 1 / 3,
        "lepton_number": 0,
    },
    "electrons": {
        "mass": 0.000511,
        "charge": -1,
        "baryon_number": 0,
        "lepton_number": 1,
    },
    # "neutrino_e": {"mass": 0, "charge": 0, "baryon_number": 0, "lepton_number": 1},
    # "neutrino_mu": {"mass": 0, "charge": 0, "baryon_number": 0, "lepton_number": 1},
    # "neutrino_tau": {"mass": 0, "charge": 0, "baryon_number": 0, "lepton_number": 1},
}

df_sm_fermions = pd.DataFrame(_sm_fermions).T


def width_phi_to_gauge(phi_mass: float, gauge_mass: float, vev: float = 10) -> float:
    """
    Calculate the partial width of the phi' boson decaying into U(1)T3R gauge boson.

    Parameters:
    - phi_mass (float): The mass of the phi' boson.
    - gauge_mass (float): The mass of the gauge boson.
    - vev (float): The vacuum expectation value (default: 10).

    Returns:
    - float: The partial width of the phi' boson decaying into U(1)T3R gauge boson.

    """
    kin_space = 1 - (2 * gauge_mass) ** 2 / phi_mass**2
    if kin_space < 0:
        return 0

    main = phi_mass**3 / (128 * np.pi * phi_mass**2 * vev**2)
    loop_correction = 1 - 4 * gauge_mass**2 / phi_mass**2 + 12 * gauge_mass**4 / phi_mass**4

    return main * (kin_space**0.5) * loop_correction


def width_phi_to_sm_fermions(phi_mass: float, fermion_mass: float, vev: float = 10) -> float:
    """
    Calculate the partial width of the phi' boson decaying into SM fermions.

    Parameters:
    - phi_mass (float): The mass of the phi' boson.
    - fermion_mass (float): The mass of the SM fermion.
    - vev (float): The vacuum expectation value (default: 10).

    Returns:
    - float: The partial width of the phi' boson decaying into SM fermions.

    """
    if phi_mass < 2 * fermion_mass:
        return 0
    main = (fermion_mass**2) * phi_mass / (16 * np.pi * vev**2)
    kin_space = 1 - (2 * fermion_mass) ** 2 / phi_mass**2
    return main * (kin_space**1.5)


def f(tau: float) -> float:
    """
    Auxiliary function for the loop integral.
    """
    if tau > 1:
        return np.arcsin(1 / np.sqrt(tau)) ** 2
    elif tau < 1:
        return -0.25 * (np.log((1 + np.sqrt(1 - tau)) / (1 - np.sqrt(1 - tau))) - 1j * np.pi) ** 2
    else:
        return 1


def loop_int(tau: float) -> float:
    """
    Calculate the loop integral for the decay width of the phi' boson.

    Parameters:
    - tau (float): four times mass squared ratio of the SM fermion to the phi' boson. \

    Returns:
    - float: The loop integral for the decay width of the phi' boson.

    """
    return 1 + (1 - tau) * f(tau)


def width_phi_to_photons(
    phi_mass: float,
    sm_fermions_data: pd.DataFrame,
    alpha_em: float = 1 / 137,
    vev: float = 10,
) -> float:
    """
    Calculate the partial width of the phi' boson decaying into photons.

    Parameters:
    - phi_mass (float): The mass of the phi' boson.
    - sm_fermions_data (pd.DataFrame): The dataframe containing the SM fermions data.
        -- The dataframe should contain the following columns:
            - mass (float): The mass of the SM fermion.
            - charge (float): The charge of the SM fermion.
            - baryon_number (float): The baryon number of the SM fermion.
            - lepton_number (float): The lepton number of the SM fermion.
    - alpha_em (float): The electromagnetic coupling constant (default: 1/137).
    - vev (float): The vacuum expectation value (default: 10).

    Returns:
    - float: The partial width of the phi' boson decaying into photons.
    """
    partial_sums = []
    main = (alpha_em**2) / (8 * (np.pi**3) * phi_mass * vev**2)
    for part, mass in sm_fermions_data.get("mass", {}).items():
        charge = sm_fermions_data.get("charge", {}).get(part, 0)
        B = sm_fermions_data.get("baryon_number", {}).get(part, 0)
        L = sm_fermions_data.get("lepton_number", {}).get(part, 0)
        color_factor = 1 / abs(B - L)
        if charge == 0:
            continue
        fermion_factor = color_factor * charge**2 * mass**2
        tau = 4 * mass**2 / phi_mass**2
        loop_factor = loop_int(tau)
        partial_sums.append(fermion_factor * loop_factor)
    sumation = np.sum(partial_sums)
    return main * np.linalg.norm(sumation * np.conj(sumation))


def width_phi_to_gluons(
    phi_mass: float,
    quark_masses: list,
    alpha_s: float = 0.118,
    vev: float = 10,
) -> float:
    """
    Calculate the partial width of the phi' boson decaying into gluons.

    Parameters:
    - phi_mass (float): The mass of the phi' boson.
    - quark_masses (list): The list of masses of the SM quarks.
    - alpha_s (float): The strong coupling constant (default: 0.118).
    - vev (float): The vacuum expectation value (default: 10).

    Returns:
    - float: The partial width of the phi' boson decaying into gluons.
    """
    main = (alpha_s**2) / (4 * np.pi**3 * phi_mass * vev**2)
    partial_sum = []
    for mass in quark_masses:
        tau = 4 * mass**2 / phi_mass**2
        loop_factor = loop_int(tau)
        partial_sum.append(mass**2 * loop_factor)
    sumation = np.sum(partial_sum)
    return main * np.linalg.norm(sumation * np.conj(sumation))


def get_all_widths(
    phi_mass: float,
    gauge_mass: float,
    sm_fermions_data: pd.DataFrame,
    alpha_em: float = 1 / 137,
    alpha_s: float = 0.118,
    vev: float = 10,
) -> dict:
    """
    Calculate the partial widths of the phi' boson decaying into all possible final states.

    Parameters:
        - phi_mass (float): The mass of the phi' boson.
        - gauge_mass (float): The mass of the gauge particle.
        - sm_fermions_data (pd.DataFrame): Dataframe containing information about Standard Model fermions.
            -- The dataframe should contain the following columns:
                - mass (float): The mass of the SM fermion.
                - charge (float): The charge of the SM fermion.
                - baryon_number (float): The baryon number of the SM fermion.
                - lepton_number (float): The lepton number of the SM fermion.
        - alpha_em (float, optional): The electromagnetic coupling constant. Defaults to 1/137.
        - alpha_s (float, optional): The strong coupling constant. Defaults to 0.118.
        - vev (float, optional): The vacuum expectation value. Defaults to 10.

    Returns:
        dict: A dictionary containing the

    """
    widths = {}

    fermion_masses = sm_fermions_data.get("mass", {})
    lightest_fermions_list = ["ups", "downs", "electrons", "neutrinos"]
    lightest_fermions_key = r"other"
    second_generation_quarks = ["charms", "stranges"]
    second_generation_quarks_key = r"$c\bar c$ + $s\bar s$"
    for fermion, mass in fermion_masses.items():
        if fermion in lightest_fermions_list:
            widths[lightest_fermions_key] = widths.get(
                lightest_fermions_key, 0
            ) + width_phi_to_sm_fermions(phi_mass=phi_mass, fermion_mass=mass, vev=vev)
        elif fermion in second_generation_quarks:
            widths[second_generation_quarks_key] = widths.get(
                second_generation_quarks_key, 0
            ) + width_phi_to_sm_fermions(phi_mass=phi_mass, fermion_mass=mass, vev=vev)
        elif fermion == "bottoms":
            widths[r"$b\bar b$"] = width_phi_to_sm_fermions(
                phi_mass=phi_mass, fermion_mass=mass, vev=vev
            )
        elif fermion == "taus":
            widths[r"$\tau^+\tau^-$"] = width_phi_to_sm_fermions(
                phi_mass=phi_mass, fermion_mass=mass, vev=vev
            )
        elif fermion == "muons":
            widths[r"$\mu^+\mu^-$"] = width_phi_to_sm_fermions(
                phi_mass=phi_mass, fermion_mass=mass, vev=vev
            )
        else:
            widths[fermion] = width_phi_to_sm_fermions(
                phi_mass=phi_mass, fermion_mass=mass, vev=vev
            )

    widths[r"$\gamma \gamma$"] = width_phi_to_photons(
        phi_mass, sm_fermions_data[sm_fermions_data["charge"] != 0], alpha_em, vev
    )
    quark_masses = [
        mass for mass in sm_fermions_data[sm_fermions_data["baryon_number"] != 0].get("mass", {})
    ]
    widths[r"$g g$"] = width_phi_to_gluons(phi_mass, quark_masses, alpha_s, vev)
    widths[r"$A^\prime A^\prime$"] = width_phi_to_gauge(phi_mass, gauge_mass, vev)
    return widths


def get_all_branching_ratios(
    phi_mass: float,
    gauge_mass: float,
    sm_fermions_data: pd.DataFrame,
    alpha_em: float = 1 / 137,
    alpha_s: float = 0.118,
    vev: float = 10,
) -> dict:
    """
    Calculate the branching ratios of the phi' boson decaying into all possible final states.

    Parameters:
        - phi_mass (float): The mass of the phi' boson.
        - gauge_mass (float): The mass of the gauge particle.
        - sm_fermions_data (pd.DataFrame): Dataframe containing information about Standard Model fermions.
            -- The dataframe should contain the following columns:
                - mass (float): The mass of the SM fermion.
                - charge (float): The charge of the SM fermion.
                - baryon_number (float): The baryon number of the SM fermion.
                - lepton_number (float): The lepton number of the SM fermion.
        - alpha_em (float, optional): The electromagnetic coupling constant. Defaults to 1/137.
        - alpha_s (float, optional): The strong coupling constant. Defaults to 0.118.
        - vev (float, optional): The vacuum expectation value. Defaults to 10.

    Returns:
        dict: A dictionary containing the branching ratios of the phi' boson decaying into all possible final states.

    """
    widths = get_all_widths(
        phi_mass=phi_mass,
        gauge_mass=gauge_mass,
        sm_fermions_data=sm_fermions_data,
        alpha_em=alpha_em,
        alpha_s=alpha_s,
        vev=vev,
    )
    total_width = sum(widths.values())
    return {key: value / total_width for key, value in widths.items()}


def calculate_branching_ratios(
    gauge_boson_mass: float,
    sm_fermions_df: pd.DataFrame,
    alpha_em: float = 1 / 137,
    alpha_s: float = 0.118,
    vev: float = 10,
    n_points: int = 1000,
    plot: bool = False,
    file_name: str = "",
):
    if file_name == "":
        file_name = f"phi_decay_branching_ratios_gauge_mass_{gauge_boson_mass}"

    phi_mass_values = np.logspace(np.log10(2.5), np.log10(340), n_points)
    branching_ratios = {}

    for phi_mass in phi_mass_values:
        for particle, ratio in get_all_branching_ratios(
            phi_mass=phi_mass,
            gauge_mass=gauge_boson_mass,
            sm_fermions_data=sm_fermions_df,
            alpha_em=alpha_em,
            alpha_s=alpha_s,
            vev=vev,
        ).items():
            if particle not in branching_ratios:
                branching_ratios[particle] = []
            branching_ratios[particle].append(ratio)
    if plot:
        plt.figure(figsize=(9, 6))
        # Define a list of line styles for better visibility for color blind people
        line_styles = ["--", "-.", ":", "-"]
        # Define a list of colors that are generally more distinguishable for color blind people
        colors = [
            "green",
            "red",
            "black",
            "blue",
            "brown",
        ]

        for index, (particle, ratios) in enumerate(branching_ratios.items()):
            if particle == "tops":
                continue
            line_style = line_styles[index % len(line_styles)]
            color = colors[index % len(colors)]
            plt.plot(
                phi_mass_values,
                ratios,
                label=particle,
                linestyle=line_style,
                color=color,
                linewidth=2.6,
            )
        plt.xlabel(r"$m(\phi^\prime)$ [GeV]", loc="right", fontsize=17)
        plt.ylabel(r"$\text{BR}(\phi^\prime \rightarrow XX)$", loc="top", fontsize=16)

        plt.yscale("log")
        plt.xscale("log")
        plt.tick_params(axis="x", labelsize=15)
        plt.tick_params(axis="y", labelsize=15)
        # plt.title(
        #     r"Branching Ratios of $\phi^\prime$ Decays, for $m_{{A'}} = {}$ GeV".format(
        #         gauge_boson_mass
        #     ),
        #     fontsize=18,
        # )
        plt.legend(fontsize=16, ncol=2, loc="lower right")

        plt.xlim(2.6, 340)

        plt.ylim(1e-6, 1)

        x_subticks = LogLocator(subs=[2, 3, 4, 5, 6, 7, 8, 9], base=10)
        y_subticks = LogLocator(subs=[2, 3, 4, 5, 6, 7, 8, 9], base=10)

        plt.gca().xaxis.set_minor_locator(x_subticks)
        plt.gca().yaxis.set_minor_locator(y_subticks)
        # plt.grid(which="both")
        plt.grid(True)
        plt.savefig(f"pdfs/{file_name}.pdf")
        plt.savefig(f"images/{file_name}.png")
        plt.show()

    branching_ratios["phi_mass"] = phi_mass_values
    branching_ratios = pd.DataFrame(branching_ratios, index=phi_mass_values)
    return branching_ratios


if __name__ == "__main__":
    alpha_em = 1 / 137
    alpha_s = 0.118
    vev = 200

    df1 = calculate_branching_ratios(
        gauge_boson_mass=0.0,
        sm_fermions_df=df_sm_fermions,
        alpha_em=alpha_em,
        alpha_s=alpha_s,
        vev=vev,
        n_points=1000,
        plot=True,
    )
    df2 = calculate_branching_ratios(
        gauge_boson_mass=180,
        sm_fermions_df=df_sm_fermions,
        alpha_em=alpha_em,
        alpha_s=alpha_s,
        vev=vev,
        n_points=1000,
        plot=True,
    )

    df1.to_csv("data/phi_decay_branching_ratios_gauge_mass_0.0.csv")
    df2.to_csv("data/phi_decay_branching_ratios_gauge_mass_180.csv")
