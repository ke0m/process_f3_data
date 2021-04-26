ROOT=/net/brick5/data3/northsea_dutch_f3
SRC=/net/brick5/data3/northsea_dutch_f3/process_f3_data/

#
# Geometry
#

# Make the source info files
${ROOT}/segy/info_new: ${SRC}/scripts/make_srcinfo_files.py
	python ${SRC}/scripts/make_srcinfo_files.py \
		--segy=${ROOT}/segy \
		--output-info-dir=$@


# Make hash map for efficient look up
${ROOT}/segy/info_new/scoords_hmap.npy: \
	${SRC}/scripts/make_hmap_scoordfile.py
	python ${SRC}/scripts/make_hmap_scoordfile.py \
		--segy=${ROOT}/segy \
		--src-info-dir=${ROOT}/segy/info_new \
		--output-hmap=$@ \
		--output-scoords=${ROOT}/segy/info_new/scoords.npy 


# Select data


#
# Velocity model
#

# Parse files and interpolate between velocity picking
# points

# Dix inversion

# Time to depth conversion


#
# Image
#

# Read from SEGY and set the proper imaging grid

