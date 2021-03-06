"""
# test_voyager_data_load.py

The hard-coded numbers in these tests can be found in the voyager_test_setup.ipynb

"""

import blimpy as bl
import numpy as np
import pylab as plt
from tests.data import voyager_fil, voyager_h5


def test_filterbank_data_load_range_freq():
    ff = bl.Filterbank(voyager_fil, f_start=8419.24, f_stop=8419.35)
    hf = bl.Filterbank(voyager_h5, f_start=8419.24, f_stop=8419.35)

    print(ff.data.shape)
    print(hf.data.shape)
    print(ff.freqs.shape)
    print(hf.freqs.shape)

    print(ff.data[0].max(), ff.data[0].argmax())
    print(hf.data[0].max(), hf.data[0].argmax())
    print(ff.data[-1].max(), ff.data[-1].argmax())
    print(hf.data[-1].max(), hf.data[-1].argmax())

    # Assert data is loaded to the same shape and has same values
    assert ff.data.shape == hf.data.shape == (16, 1, 39371)
    assert np.allclose(ff.data, hf.data)

    # Check the Voyager carrier has the known amplitudes at first and last integration
    assert np.allclose(ff.data[0].max(), hf.data[0].max(), 3.09333e+11)
    assert np.allclose(ff.data[-1].max(), hf.data[-1].max(), 2.74257e+11)

    # Check the tone is in the same bin for both
    assert ff.data[0].argmax()  == hf.data[0].argmax() == 18960
    assert ff.data[-1].argmax() == hf.data[-1].argmax() == 18997

    plt.subplot(2,1,1)
    ff.plot_spectrum()

    plt.subplot(2,1,2)
    hf.plot_spectrum()
    plt.tight_layout()


def test_waterfall_data_load_range_freq():
    fw = bl.Waterfall(voyager_fil, f_start=8419.24, f_stop=8419.35)
    hw = bl.Waterfall(voyager_h5, f_start=8419.24, f_stop=8419.35)

    print(fw.data.shape)
    print(hw.data.shape)
    print(hw.data[0].max(), hw.data[0].argmax())
    print(fw.data[0].max(), fw.data[0].argmax())
    print(hw.data[-1].max(), hw.data[-1].argmax())
    print(fw.data[-1].max(), fw.data[-1].argmax())

    # Assert data is loaded to the same shape and has same values
    assert hw.data.shape == fw.data.shape == (16, 1, 39370)
    assert np.allclose(hw.data, fw.data)

    # Check the Voyager carrier has the known amplitudes at first and last integration
    assert np.allclose(hw.data[0].max(), fw.data[0].max(), 3.09333e+11)
    assert np.allclose(hw.data[-1].max(), fw.data[-1].max(), 2.74257e+11)

    # Check the tone is in the same bin for both
    assert hw.data[0].argmax() == fw.data[0].argmax() == 18959
    assert hw.data[-1].argmax() == fw.data[-1].argmax() == 18996

    # And plot(
    plt.subplot(2,1,1)
    fw.plot_spectrum()

    plt.subplot(2,1,2)
    hw.plot_spectrum()
    plt.tight_layout()

def test_grab_data_works_across_all_fil_h5():

    ff = bl.Filterbank(voyager_fil)
    hf = bl.Filterbank(voyager_h5)
    fw = bl.Waterfall(voyager_fil)
    hw = bl.Waterfall(voyager_h5)
    all_readers = [ff, hf, fw, hw]

    for ii, rr in enumerate(all_readers):
        f, d = rr.grab_data(f_start=8419.29, f_stop=8419.30)
        print(f.shape, d.shape)
        assert f.shape == (3580,)
        assert d.shape == (16, 3580)

    for ii, rr in enumerate(all_readers):
        f, d = rr.grab_data(f_start=8419.29685, f_stop=8419.2971)
        print(f.shape, d.shape)
        assert f.shape == (91,)
        assert d.shape == (16, 91)

if __name__ == "__main__":
    test_filterbank_data_load_range_freq()
    test_waterfall_data_load_range_freq()
    test_grab_data_works_across_all_fil_h5()
