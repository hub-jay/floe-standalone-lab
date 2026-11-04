# =============================================================================
# setup.jl -- one-time installation of the Julia packages this project needs.
#
# Run ONCE (and again only if packages change), from the julia> prompt with
# this folder as the current folder:
#     include("setup.jl")
#
# If Project.toml + Manifest.toml already exist (e.g. after cloning from
# GitHub), this installs the exact package versions recorded in them.
# Otherwise it adds the packages and creates those two files.
# =============================================================================
using Pkg
Pkg.activate(@__DIR__)

const PACKAGES = ["StructArrays", "NCDatasets"]

if isfile(joinpath(@__DIR__, "Manifest.toml"))
    println("Installing exact package versions from Manifest.toml ...")
    Pkg.instantiate()
else
    println("First-time set-up: adding ", join(PACKAGES, ", "), " ...")
    Pkg.add(PACKAGES)
end
Pkg.precompile()
println("\nSet-up complete. You can now run, for example:")
println("    include(\"scripts/run_simulation.jl\")")
