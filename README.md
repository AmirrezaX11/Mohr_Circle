# Mohr's Circle

A modern and lightweight **Mohr's Circle** calculator and visualization tool built with **Python and Tkinter**.

This application is designed for engineering students and anyone who needs a simple way to calculate and visualize the 2D stress state using Mohr's Circle.

## ✨ Features

* 📐 Calculate Mohr's Circle from:

  * Normal stress in X direction (`σx`)
  * Normal stress in Y direction (`σy`)
  * Shear stress (`τxy`)
* 📊 Interactive graphical visualization of Mohr's Circle
* 🎯 Automatically calculates:

  * Average normal stress (`σavg`)
  * Circle radius (`R`)
  * Maximum principal stress (`σmax`)
  * Minimum principal stress (`σmin`)
  * Principal stress angle (`θ`)
* 🔄 Support for:

  * MPa
  * ksi
* 🧮 Automatic graph scaling
* 🎨 Clean and modern graphical interface
* 🖥️ Windows `.exe` build support
* 🧹 Clear button for quickly resetting inputs
* 📍 Stress points and important circle intersections are labeled directly on the graph

## 🖼️ Preview

> Add a screenshot of the application here.

```text
docs/
└── screenshot.png
```

Then replace this section with:

```markdown
![Mohr's Circle](docs/screenshot.png)
```

## 🛠️ Built With

* **Python 3**
* **Tkinter** — Graphical User Interface
* **Pillow** — Image and logo handling
* **PyInstaller** — Windows executable packaging
* **Math** — Stress and Mohr's Circle calculations

## 📋 Requirements

For running the Python version:

* Python 3.10+
* Pillow

For creating the Windows executable:

* Windows 10/11
* Python 3
* PyInstaller
* Pillow

## 🚀 Running the Python Version

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Mohrs-Circle.git
cd Mohrs-Circle
```

Install the required package:

```bash
python -m pip install pillow
```

Run the application:

```bash
python mohrs_circle.py
```

## 🪟 Building the Windows `.exe`

The repository includes a batch script that automatically installs the required dependencies and builds the executable.

Simply run:

```text
build_exe.bat
```

Or build manually with PyInstaller:

```bash
python -m pip install pyinstaller pillow
```

Then:

```bash
python -m PyInstaller --clean --noconfirm --onefile --windowed --name "Mohrs_Circle" --icon "mohrs_circle.ico" --add-data "a_clean_modern_vector_style_graphic_icon_illus.png;." "mohrs_circle.py"
```

After a successful build, the executable will be located at:

```text
dist/Mohrs_Circle.exe
```

## 📁 Project Structure

```text
Mohrs-Circle/
│
├── mohrs_circle.py
├── mohrs_circle.spec
├── mohrs_circle.ico
├── a_clean_modern_vector_style_graphic_icon_illus.png
├── build_exe.bat
├── requirements.txt
├── README.md
│
└── dist/
    └── Mohrs_Circle.exe
```

## 📐 Calculations

The application uses the standard equations for a 2D stress state.

### Average Normal Stress

$$
\sigma_{avg} = \frac{\sigma_x + \sigma_y}{2}
$$

### Mohr's Circle Radius

$$
R =
\sqrt{
\left(
\frac{\sigma_x-\sigma_y}{2}
\right)^2
+
\tau_{xy}^2
}
$$

### Principal Stresses

$$
\sigma_{max} = \sigma_{avg}+R
$$

$$
\sigma_{min} = \sigma_{avg}-R
$$

### Principal Stress Angle

$$
\theta =
\frac{1}{2}
\tan^{-1}
\left(
\frac{2\tau_{xy}}
{\sigma_x-\sigma_y}
\right)
$$

The application calculates the angle using `atan2` to correctly handle the sign and quadrant of the stress state.

## 🎓 Intended Use

This project is mainly intended as an educational and engineering calculation tool, particularly for:

* Civil Engineering students
* Mechanical Engineering students
* Structural Engineering students
* Strength of Materials courses
* Mechanics of Materials courses
* Stress analysis exercises

It can be useful for checking hand calculations and visualizing how normal and shear stresses relate to principal stresses.

## ⚠️ Disclaimer

This software is intended for **educational and reference purposes**.

Always verify engineering calculations independently before using the results in professional engineering design or safety-critical applications.

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome.

If you find a bug or have an idea for improving the application:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Commit your changes
5. Open a Pull Request

## 📄 License

This project is open source.

You may add a specific license such as **MIT License** by including a `LICENSE` file in the repository.

---

### 👨‍💻 Author

**Amirreza Abdi**

Built with Python 🐍 and Tkinter.
