#/bin/sh
mkdir -p "systems"
# makes directory called system if it doesnt exist
path="$(pwd)"
# gets current path
path="$path"
repository="https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue.git"
if [ -d "open_exoplanet_catalogue/systems" ] 
# if open_exoplanet_catalogue exists
then
    git fetch $repository
# update the folder
else 
    git clone $repository
# clone the repository
fi
cd open_exoplanet_catalogue
cp -r systems "$path"