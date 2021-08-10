from Ei_ref_scan import EiRefScan
from Ei_Library import Library
from outputer import dump_ei_list
import editor

ei = ["ei1", "ei2", "ei3", "ei4", "ei5", "p420", "p560"]
ei_title = ["EI-1", "EI-2", "EI-3", "EI-4", "EI-5", "P-420", "P-560"]
chem_name = ["2-Aminopyridine", "Quinine Sulphate", "Coumarin-153",
             "DCM", "LDS-751", "NaSal", "YAG:Ce"]
sample_type = ["liquid", "liquid", "liquid", "liquid", "liquid",
               "solid", "solid"]
ref_em_range = ["327 440", "395 571", "485 680", "557 739", "645 881", "496 710", "496 710"]
qy_em_range = ["315 500", "380 650", "-", "-", "-", "360 600", "480 750"]
qy = ["74", "57", "-", "-", "-", "43", "90", "95"]
filename = ["Scan_vis_ei1 - Copy.txt", "Scan_vis_ei2 - Copy.txt", "Scan_vis_ei3 - Copy.txt",
            "Scan_vis_ei4 - Copy.txt", "Scan_vis_ei5 - Copy.txt", "Scan_vis_p420 - Copy.txt",
            "Scan_vis_p560 - Copy.txt"]
library = Library()

for i in range(len(ei)):
    scan = EiRefScan()
    scan.key = ei[i]
    scan.name = ei_title[i]
    scan.product_name = chem_name[i]
    scan.sample_type = sample_type[i]
    scan.ref_emission_range = ref_em_range[i]
    scan.qy = qy[i]
    scan.qy_emission_range = qy_em_range[i]
    #editor.fix_format("scans/"+filename[i])
    scan.add_scan("scans/"+filename[i]+" modified")
    library.library = scan

dump_ei_list(library)

