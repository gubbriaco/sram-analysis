from matplotlib import pyplot as plt
import os
from utils.path import images
from models.ops import save_image


def graphical_seevinck_comparative_analysis(w_ax_standard_hold, snm_standard_hold, snm_standard_read, snm_seevinck_hold,
                                            snm_seevinck_read, plot_lock):
    w_ax_hold = w_ax_standard_hold
    print("{:<20} {:<30} {:<30}".format("w_ax [u]", "%difference snm(hold) [%]", "%difference snm(read) [%]"))
    percentage_difference_snm_hold = []
    percentage_difference_snm_read = []
    for w_ax, s11, s21, s12, s22 in zip(w_ax_hold, snm_standard_hold, snm_standard_read, snm_seevinck_hold,
                                        snm_seevinck_read):
        percentage_difference_snm_hold_value = (abs(s11 - s12) / ((s11 + s12) / 2)) * 100
        percentage_difference_snm_read_value = (abs(s21 - s22) / ((s21 + s22) / 2)) * 100
        percentage_difference_snm_hold.append(percentage_difference_snm_hold_value)
        percentage_difference_snm_read.append(percentage_difference_snm_read_value)
        print("{:<20} {:<30} {:<30}".format(f'{w_ax}', f'{percentage_difference_snm_hold_value}',
                                            f'{percentage_difference_snm_read_value}'))
    with plot_lock:
        fig_percentage_difference_comparative_analysis = plt.figure(figsize=(12, 4))
        plt.plot(w_ax_hold, percentage_difference_snm_hold, '-*', label='diff_snm_hold', color='blue')
        plt.plot(w_ax_hold, percentage_difference_snm_read, '-*', label='diff_snm_read', color='green')
        plt.ylabel('%difference_snm [%]')
        plt.xlabel('w_ax [u]')
        plt.legend(['%diff_snm_hold', '%diff_snm_read'])
        plt.title('%DIFFERENCE SNM AS W_AX CHANGES')
        plt.tight_layout()
        plt.grid()
        save_image(image_path=os.path.join(images, "difference_snm_w_ax.png"), plt=plt)
        plt.show()
