import random
import tkinter as tk
from tkinter import simpledialog, messagebox
import pyperclip  # Bibliothèque pour copier du texte dans le presse-papiers
from cryptography.fernet import Fernet

# Création de la clé de chiffrement et de l'objet Fernet
key = Fernet.generate_key()
cipher = Fernet(key)

# Spécification du chemin de stockage pour la clé
chemin_stockage_cle = "C:\\Users\\Forster\\Documents\\ProjetPython1.0\\cle_de_chiffrement.key"

# Spécification du chemin de stockage pour les mots de passe chiffrés
chemin_stockage_mdp = "C:\\Users\\Forster\\Documents\\ProjetPython1.0\\mots_de_passe_chiffres.txt"

# Création de la fenêtre principale
root = tk.Tk()
root.withdraw()  # Cache la fenêtre principale de Tk

# Création de variables pour les lettres, chiffres et symboles
lettre = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
nombre = "0123456789"
symbole = "!ù*$&§%µ£#{}[]\@|€()"

# Concaténation pour créer les groupes de caractères avec et sans symboles
caractere = lettre + lettre.lower() + nombre + symbole
caractere_sans_symbole = lettre + lettre.lower() + nombre

def copier_dans_presse_papier(texte):
    pyperclip.copy(texte)
    messagebox.showinfo("Copié !", "Le mot de passe a été copié dans le presse-papiers.")

def stocker_mot_de_passe_chiffre(mdp_chiffre):
    with open(chemin_stockage_mdp, "ab") as file:
        file.write(mdp_chiffre + b"\n")

# Stockage de la clé de chiffrement dans un fichier
with open(chemin_stockage_cle, "wb") as file:
    file.write(key)

while True:
    try:
        # Demande de la longueur et du nombre de mots de passe à l'utilisateur via des boîtes de dialogue
        longueurMDP = simpledialog.askinteger("Longueur du mot de passe", "Entrez la longueur du mot de passe:")
        nombredeMDP = simpledialog.askinteger("Nombre de mots de passe", "Entrez le nombre de mot de passe à afficher:")
        
        # Vérification si la longueur ou le nombre de mots de passe est inférieur ou égal à zéro
        if longueurMDP <= 0 or nombredeMDP <= 0:
            raise ValueError("La longueur et le nombre de mots de passe doivent être supérieurs à zéro.")
        
        caractere_speciaux = messagebox.askyesno("Caractères spéciaux", "Dois-je mettre des caractères spéciaux dans le mot de passe ?")

        # Génération des mots de passe avec ou sans caractères spéciaux selon la réponse
        for i in range(nombredeMDP):
            mdp = ""
            for j in range(longueurMDP):
                if caractere_speciaux:
                    cmdp = random.choice(caractere)
                else:
                    cmdp = random.choice(caractere_sans_symbole)
                mdp += cmdp
            
            # Chiffrement du mot de passe
            mdp_chiffre = cipher.encrypt(mdp.encode())
            
            # Stockage du mot de passe chiffré
            stocker_mot_de_passe_chiffre(mdp_chiffre)
            
            # Copie dans le presse-papiers si demandé
            if messagebox.askokcancel("Mot de passe généré", f'Votre mot de passe est: {mdp}\nVoulez-vous le copier dans le presse-papiers?'):
                copier_dans_presse_papier(mdp)
                
            messagebox.showinfo("Mot de passe généré", f'Votre mot de passe est: {mdp}')
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
        continue
    except TypeError:
        break
