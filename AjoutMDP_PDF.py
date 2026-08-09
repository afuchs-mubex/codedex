#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import tempfile
import shutil
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import messagebox


def ajouter_liens_words(pdf_input, mot_de_passe, threshold=0.6, debug=False):
    """
    Ouvre un fichier PDF, authentifie si nécessaire, effectue des modifications
    (par exemple, ajouter des liens) et sauvegarde le document en écrasant le fichier source.
    """
    # Ouvrir le document PDF
    doc = fitz.open(pdf_input)

    # Vérifier s'il est chiffré et tenter l'authentification
    if doc.is_encrypted:
        if not doc.authenticate(mot_de_passe):
            doc.close()
            raise ValueError("Mot de passe incorrect, impossible d'ouvrir le document.")


    # Sauvegarder dans un fichier temporaire pour éviter les conflits d'accès
    temp_fd, temp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(temp_fd)  # On ferme le descripteur pour que PyMuPDF puisse écrire
    doc.save(temp_path,
             encryption=fitz.PDF_ENCRYPT_AES_256,  # Chiffrement AES 256 bits
             owner_pw=mot_de_passe,
             user_pw="",
             permissions=fitz.PDF_PERM_PRINT)
    doc.close()

    # Remplacer le fichier source par le fichier temporaire (écrase le fichier original)
    shutil.move(temp_path, pdf_input)
    print(f"Le fichier modifié a été enregistré et a écrasé l'original : {pdf_input}")

if __name__ == "__main__":
    # Vérifier que le script a reçu le chemin d'un fichier PDF
    if len(sys.argv) < 2:
        print(f"Usage : {sys.argv[0]} fichier_pdf")
        sys.exit(1)
    
    # Le fichier PDF sur lequel on a fait un clic droit est passé en argument
    pdf_input = sys.argv[1]
    mot_de_passe = "ABC"  # Vous pouvez modifier ou paramétrer ce mot de passe si nécessaire

    # Instancier Tkinter pour les pop-ups
    root = tk.Tk()
    root.withdraw()  # On cache la fenêtre principale

    try:
        ajouter_liens_words(pdf_input, mot_de_passe=mot_de_passe, threshold=0.6, debug=True)
    except Exception as e:
        messagebox.showerror("Erreur", f"Le mot de passe n'a pas pu être ajouté :\n{e}")
        sys.exit(1)
    else:
        messagebox.showinfo("Succès", "Le mot de passe a correctement été ajouté au PDF.")
    finally:
        root.destroy()