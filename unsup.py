# USAGE:
#   1. set the variables below with
#      the details of the project and group
#   2. _for each task_ create a folder inside
#      the chosen root folder (default: 'src/')
#      FILENAME SYNTAX: <id>@<desc>
GROUP = [
    {"matr": "898685", "name": "Alberto Mosconi"},
    {"matr": "898685", "name": "Alberto Mosconi"},
]
LAB_NUMBER = "1"
LAB_TITLE = "Title of the lab"
LAB_DATE = "DD/MM/2023"
LAB_DESCRIPTION = "Here you can describe the lab experience and the aim of this report (see slide from the instructor)."
TAKEHOME_MESSAGE = (
    "In this lab we learned about this thing and especially this other things."
)

IMG_FOLDER = "src"
OUTPUT_DIR = "out"

import os
from typing import TextIO, List
import shutil


def parse_fn(fn: str):
    fn_id, desc = fn.split("@")
    return fn_id, desc


def gen_latex_lines() -> List[str]:
    lines: List[str] = []
    tasks_folders = sorted(os.listdir(IMG_FOLDER))
    for f_task in tasks_folders:
        task_id, task_desc = parse_fn(f_task)
        # print(f"task {task_id}: {task_desc}")

        lines.append("\\section*{Task " + task_id + ": " + task_desc + "}\n")

        path_task = os.path.join(IMG_FOLDER, f_task)
        subtasks_folders = sorted(os.listdir(path_task))

        for f_subtask in subtasks_folders:
            sub_id, desc = parse_fn(f_subtask)
            lines.append("\\subsection*{" + desc + "}\n")

            path_subtask = os.path.join(path_task, f_subtask)
            subtask_images = sorted(os.listdir(path_subtask))
            for sub_img in subtask_images:
                subimg_id, subimg_desc = parse_fn(sub_img)
                label = task_id + "-" + sub_id + "-" + subimg_id
                latex = (
                    """\\begin{figure}[h]
\\centering
\\includegraphics[width=\\textwidth]{figures/"""
                    + label
                    + """}
\\label{fig:"""
                    + label
                    + """}
\\end{figure}

"""
                )
                lines = [*lines, *latex.splitlines()]

                shutil.copy(
                    os.path.join(path_subtask, sub_img),
                    os.path.join(OUTPUT_DIR, "figures", f"{label}.png"),
                )

    return lines


def write_lines_in_file(file: TextIO, lines: List[str]):
    file.write("\n".join(lines))
    file.write("\n")


PREAMBLE = (
    """%%% Preamble %%%
\\documentclass[a4paper,titlepage]{book}
\\usepackage[margin=20mm]{geometry}
\\usepackage[suftesi]{frontespizio}
\\usepackage[T1]{fontenc}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage{listings}
\\usepackage{textcomp}
\\usepackage{multirow}
\\usepackage{multicol}
\\usepackage{booktabs}
\\usepackage{graphicx}
\\usepackage{floatflt}
\\usepackage{epsfig}
\\usepackage{pstricks}
\\usepackage{subfigure}
\\usepackage[labelfont=bf, font=scriptsize]{caption}
\\usepackage[italian]{varioref}
\\usepackage{color}
\\usepackage{tikz}
\\usepackage{caption}
\\usepackage{pgfplots}
\\usepackage{comment}
\\usepackage{lipsum}
\\pgfplotsset{compat=1.16}

%%% Front page %%%
% DO NOT MODIFY LINES ENDING BY CTT (Can't Touch This).
% TO BE MODIFIED: date, title, students' names, student number. 

% IMPORTANT NOTICE. Once you have modified the frontal page (e.g., including your names), please clear the cache of this file. Here are the - very simple - instructions to do it: https://www.overleaf.com/learn/how-to/Clearing_the_cache


%% Beginning of your document %%
\\begin{document}


\\begin{frontespizio}
% https://it.overleaf.com/learn/latex/Questions/How_do_I_use_the_frontespizio_package%3F
% https://ctan.mirror.garr.it/mirrors/ctan/macros/latex/contrib/frontespizio/frontespizio.pdf

% \\Filigrana[height=2cm, before=0.05, after=1.95]{Figures/AI4ST} % CTT
% \\Logo{Figures/logo_800anni}
% \\Preambolo{\\renewcommand{\\frontlogosep}{3cm}}


% Margins: {left}{bottom}{right}{top}
\\Margini{2cm}{1.5cm}{3cm}{2cm} %CTT

\\Istituzione{University of Milano-Bicocca, University of Milano, University of Pavia} % CTT
\\Divisione{Artificial Intelligence for Science and Technology} % CTT
\\Scuola{Course of Unsupervised Learning - Academic Year 2022-2023} % CTT

\\Annoaccademico{2022-2023}
\\Titoletto{Lab Report} % CTT
\\Titolo{Laboratory session no. """
    + LAB_NUMBER
    + """: """
    + LAB_TITLE
    + """}
\\Sottotitolo{"""
    + LAB_DATE
    + """}

\\Candidato["""
    + GROUP[0]["matr"]
    + """]{"""
    + GROUP[0]["name"]
    + """}
\\Candidato["""
    + GROUP[1]["matr"]
    + """]{"""
    + GROUP[1]["name"]
    + """}
 
\\NRelatore{Instructors}{Instructors} % CTT
\\Relatore{Dr. Giulia Cisotto} % CTT
\\Relatore{Prof. Fabio Stella} 


\\end{frontespizio}


\\IfFileExists{\\jobname-frn.pdf}{}{%
\\immediate\\write18{pdflatex \\jobname-frn}} % ASSOLUTAMENTE CTT, è il comando che materialmente vi genera il frontespizio.

\\newpage

\\section*{Short description of this lab session}

"""
    + LAB_DESCRIPTION
    + """

"""
)

FOOTER = (
    """\\section*{Take-home message}

"""
    + TAKEHOME_MESSAGE
    + """

\\end{document}
% Credits: modified from previous template by Giulia Cisotto (last update January 18th 2023).
% Credits: modified from template of Dr. Enia: https://it.overleaf.com/latex/templates/template-relazione-di-laboratorio-i-degrees-anno-dfa-unipd/smvqmktmwsfd
%% Credits: 2008 Enrico Gregorio: https://www.ctan.org/tex-archive/macros/latex/contrib/frontespizio"""
)

do_build = True
if os.path.isdir(OUTPUT_DIR):
    do_build = input("output dir already exists. override? [y/n]") == "y"
    if do_build:
        shutil.rmtree(OUTPUT_DIR)

if do_build:
    print("building report...")
    os.mkdir(OUTPUT_DIR)
    os.mkdir(os.path.join(OUTPUT_DIR, "figures"))
    OUTPUT_FILE = "report.txt"
    with open(os.path.join(OUTPUT_DIR, OUTPUT_FILE), "w") as fout:
        write_lines_in_file(fout, PREAMBLE.split("\n"))
        write_lines_in_file(fout, gen_latex_lines())
        write_lines_in_file(fout, FOOTER.split("\n"))
    print("done.")
else:
    print("execution aborted.")
