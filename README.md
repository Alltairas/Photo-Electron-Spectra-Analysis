# Photoelectron Spectra of Krypton: Gaussian Peak Analysis

Analysis of experimental **photoelectron spectra (PES) of krypton** ionised by attosecond XUV pulses. The
pulses come from high-harmonic generation (HHG) in xenon. The goal is to recover the kinetic-energy peaks
and the Kr 4p spin–orbit splitting by Gaussian fitting, then compare the results with the literature.

> Lab report: M2 Physics (OPHO), UE *Spectroscopie Avancée*, Université Claude Bernard Lyon 1 — Aras Selahiye

## Experimental setup (summary)

- Ti:Sapphire laser: 800 nm, 2 mJ, 5 kHz, femtosecond NIR pulses
- An HHG chamber with xenon produces an XUV attosecond pulse train; an aluminium filter removes the
  leftover NIR
- A photoelectron spectrometer measures the electrons emitted by krypton gas

## Analysis

The 5 spectra (`Kr_PES_0.txt` … `Kr_PES_4.txt`, columns: energy [eV], signal) are processed with:

| Script | Role |
|--------|------|
| `singleGaussPeakFit.py` | Interactive fit of a single Gaussian peak on an x-interval you choose |
| `GaussianParameterFinder.py` | Batch fit of 6 peaks per spectrum, with intervals read from `fitting_intervals.txt` |
| `MultipleGaussianFit.py` | Multi-Gaussian fit of overlapping peaks, e.g. the two spin–orbit components |
| `Figure_generation_Kr_PES_0_to_4.py` | Raw-data overlays, and peak means / resolutions with 95 % confidence intervals |

For each peak the fit gives the amplitude, mean energy, standard error, σ, FWHM and resolution (FWHM /
mean). All results are collected in `TotalParams.txt`.

## Repository layout

```
TP_PES_Selahiye_Aras/            Final scripts + report (PDF)
Krypton Photoelectron Spectra/   Raw data, fit parameters, figures, working scripts
Rapport/                         Figures used in the report
report docs/                     Course material and references
Loriot_2020_J._Phys._Photonics_2_024003.pdf   Reference article
```

## Usage

```bash
pip install numpy pandas matplotlib scipy
cd "Krypton Photoelectron Spectra"
python GaussianParameterFinder.py
```

## Reference

V. Loriot *et al.*, *J. Phys. Photonics* **2**, 024003 (2020)
