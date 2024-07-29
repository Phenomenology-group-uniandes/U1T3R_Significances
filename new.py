xu_mass = 1000
top_mass = 172.5
mu_mass = 0.10566
bottom_mass = 4.7
LambdaR = math.sqrt(2)
LambdaL = 1.0 * LambdaR

vev_h = 246
vev_phi = 2 * top_mass * xu_mass / (LambdaL * LambdaR * vev_h)

print("vev_phi", vev_phi)

top_couplings = get_couplings(
    fermion_mass=top_mass,
    vector_fermion_mass=xu_mass,
    vev_h=vev_h,
    vev_phi=vev_phi,
    LambdaRatio=LambdaL / LambdaR,
)

mu_couplings = get_couplings(
    fermion_mass=mu_mass,
    vector_fermion_mass=xu_mass,
    vev_h=vev_h,
    vev_phi=vev_phi,
    LambdaRatio=LambdaL / LambdaR,
)

botom_couplings = get_couplings(
    fermion_mass=bottom_mass,
    vector_fermion_mass=xu_mass,
    vev_h=vev_h,
    vev_phi=vev_phi,
    LambdaRatio=LambdaL / LambdaR,
)

tau_couplings = get_couplings(
    fermion_mass=1.777,
    vector_fermion_mass=xu_mass,
    vev_h=vev_h,
    vev_phi=vev_phi,
    LambdaRatio=LambdaL / LambdaR,
)

neutrino_couplings = get_couplings(
    fermion_mass=0.0000022,
    vector_fermion_mass=xu_mass,
    vev_h=vev_h,
    vev_phi=vev_phi,
    LambdaRatio=LambdaL / LambdaR,
)

mg5_params = {
    # mg5_key: value
    "pivev": top_couplings.get("V"),
    "mxu": xu_mass,
    "mxd": xu_mass,
    "mxl": xu_mass,
    "mxv": xu_mass,
    "mxu__2": xu_mass,
    "mxd__2": xu_mass,
    "mxl__2": xu_mass,
    "mxv__2": xu_mass,
    "lamLu": top_couplings.get("LambdaL"),
    "lamRu": top_couplings.get("LambdaR"),
    "thetauL": top_couplings.get("thetaL"),
    "C1Lu": top_couplings.get("C1L"),
    "C2Lu": top_couplings.get("C2L"),
    "C1Ru": top_couplings.get("C1R"),
    "C2Ru": top_couplings.get("C2R"),
    "lamLd": botom_couplings.get("LambdaL"),
    "lamRd": botom_couplings.get("LambdaR"),
    "thetadL": botom_couplings.get("thetaL"),
    "C1Ld": botom_couplings.get("C1L"),
    "C2Ld": botom_couplings.get("C2L"),
    "C1Rd": botom_couplings.get("C1R"),
    "C2Rd": botom_couplings.get("C2R"),