#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import sys, logging, requests, time, math

botToken = sys.argv[1]  # param 0 = nom script et 1 = token
print("VoTrE ToKeN eSt :", botToken)
print("On LaNce Le bOt !")

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

RESTAURANTS_CHOIX, SORTIE_CHOIX, SORTIE_RECOMMENDATIONS, RESTAURANT_DETAIL, RESTAURANT_RESULTATS, START, TRANSPORT = range(
    7)


def start(bot, update):
    reply_keyboard = [['Aller manger', 'Sortir']]

    update.message.reply_text(
        'Bonjour, je suis Geneva Bot !. '
        'Écrivez /cancel pour arrêter la conversation ou /transport pour accéder aux fonctionnalités de transport.\n\n'
        'Que voulez-vous faire ?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return START


# Affiche liste des types de resto
def resto_type_liste(bot, update):
    reply_keyboard = [['Italien', 'Asiatique', 'Grecque', 'Portugaise', 'Suisse']]
    update.message.reply_text(
        'Quel type de nourriture vous tente le plus ? '
        " ! Si vous avez changé d'avis entrez /retour",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return RESTAURANTS_CHOIX


# affiche la liste des restaurants peu importe le choix
def restaurant_liste(bot, update):
    user = update.message.from_user
    logger.info("Type restaurant of %s: %s", user.first_name, update.message.text)
    update.message.reply_text("Je vois, vous aimez la cuisine " + update.message.text +
                              " ! Si vous avez changé d'avis entrez /retour",
                              reply_markup=ReplyKeyboardRemove())

    # affichage liste restaurants
    reply_keyboard = [['Kebab House', 'Pizza Express', 'Kookeat', 'Tasty chicken spot', 'Punjabi']]
    update.message.reply_text(
        'Voici les restaurant correspondants à vos criètre : \n '
        '- Kebab House \n'
        '- Pizza Express \n'
        '- Kookeat \n'
        '- Tasty chicken spot \n'
        '- Punjabi \n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return RESTAURANT_RESULTATS


# Affiche detail d'un resto (peu importe) avec une map
def restaurant_detail(bot, update):
    # Affichage detail de base
    user = update.message.from_user
    logger.info("Detail restaurant of %s: %s", user.first_name, update.message.text)
    update.message.reply_text("Detail : Turc Pizza Oriental Kebab "
                              " ! Si vous avez changé d'avis entrez /retour",
                              reply_markup=ReplyKeyboardRemove())

    # Affichage map message.reply latitude longitude
    update.message.reply_location(25.0043432, -71.0164529)
    return RESTAURANT_DETAIL


# Affiche liste des types de sorties
def sortie_type_liste(bot, update):
    logger.info("Affichage liste de sorties")
    reply_keyboard = [['Musée', 'Bar', 'Club', 'Restaurant']]
    update.message.reply_text(
        'Quel genre de sortie vous tente le plus ? '
        " ! Si vous avez changé d'avis entrez /retour",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return SORTIE_CHOIX


def bar_recommendation(bot, update):
    user = update.message.from_user
    logger.info("Recommendations of %s: %s", user.first_name, update.message.text)
    update.message.reply_text("Top 3 des Bars : "
                              " ! Si vous avez changé d'avis entrez /retour",
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("1 : L'éléphant dans la canette ",
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("2 : MET Rooftop Lounge",
                              reply_markup=ReplyKeyboardRemove())

    update.message.reply_text("3 : Atelier Cocktail Club",
                              reply_markup=ReplyKeyboardRemove())
    return SORTIE_RECOMMENDATIONS


def club_recommendation(bot, update):
    user = update.message.from_user
    logger.info("Recommendations of %s: %s", user.first_name, update.message.text)
    update.message.reply_text("Top 3 des Club : "
                              " ! Si vous avez changé d'avis entrez /retour",
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("1 : Le Baroque club ",
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("2 : Java Club",
                              reply_markup=ReplyKeyboardRemove())

    update.message.reply_text("3 : Moulin Rouge",
                              reply_markup=ReplyKeyboardRemove())
    return SORTIE_RECOMMENDATIONS


def musee_recommendation(bot, update):
    user = update.message.from_user
    logger.info("Recommendations of %s: %s", user.first_name, update.message.text)
    update.message.reply_text("Top 3 des Club : "
                              " ! Si vous avez changé d'avis entrez /retour",
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("1 : Musée d'ethnographie de Genève ",
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("2 : Musée d'art et d'histoire",
                              reply_markup=ReplyKeyboardRemove())

    update.message.reply_text("3 : Musée d'histoire naturelle",
                              reply_markup=ReplyKeyboardRemove())
    return SORTIE_RECOMMENDATIONS


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Adieu bonne soirée !',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


# Partie transport

def appeler_opendata(path):
    url = "http://transport.opendata.ch/v1/" + path
    reponse = requests.get(url)
    return reponse.json()


def calcul_temps_depart(timestamp):
    seconds = timestamp - time.time()
    minutes = math.floor(seconds / 60)
    if minutes < 1:
        return "FAUT COURIR!"
    if minutes > 60:
        return "> {} h.".format(math.floor(minutes / 60))
    return "dans {} min.".format(minutes)


# Preparation des messages

def afficher_arrets(update, arrets):
    logger.info("Affichage des arrets")
    texte_de_reponse = "Voici les arrets:\n"
    for station in arrets['stations']:
        if station['id'] is not None:
            texte_de_reponse += "\n/a" + station['id'] + " " + station['name']
    update.message.reply_text(texte_de_reponse)


def afficher_departs(update, departs):
    logger.info("Affichage des departs")
    texte_de_reponse = "Voici les prochains departs:\n\n"
    for depart in departs['stationboard']:
        texte_de_reponse += "{} {} dest. {} - {}\n".format(
            depart['category'],
            depart['number'],
            depart['to'],
            calcul_temps_depart(depart['stop']['departureTimestamp'])
        )
    texte_de_reponse += "\nAfficher a nouveau: /a" + departs['station']['id']

    coordinate = departs['station']['coordinate']
    update.message.reply_location(coordinate['x'], coordinate['y'])
    update.message.reply_text(texte_de_reponse)


# Les differentes reponses

def bienvenueTransport(bot, update):
    update.message.reply_text("Merci d'envoyer votre localisation (via piece jointe ou simplement en texte)")
    logger.info("Passage a l'etat TRANSPORT")
    return TRANSPORT


def lieu_a_chercher(bot, update):
    resultats_opendata = appeler_opendata("locations?query=" + update.message.text)
    logger.info("Recherche opendata")
    afficher_arrets(update, resultats_opendata)


def coordonnees_a_traiter(bot, update):
    location = update.message.location
    logger.info("Traitement des coordonnees")
    resultats_opendata = appeler_opendata("locations?x={}&y={}".format(location.latitude, location.longitude))
    afficher_arrets(update, resultats_opendata)


def details_arret(bot, update):
    logger.info("Affichage detail des arrets")
    arret_id = update.message.text[2:]
    afficher_departs(update, appeler_opendata("stationboard?id=" + arret_id))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(botToken)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('transport', bienvenueTransport)],

        states={
            START: [
                RegexHandler('^(Aller manger)$', resto_type_liste),
                RegexHandler('^(Sortir)$', sortie_type_liste),
                CommandHandler('retour', start),
                CommandHandler('transport', bienvenueTransport)
            ],

            RESTAURANTS_CHOIX: [
                RegexHandler('^(Italien|Asiatique|Grecque|Portugaise|Suisse)$', restaurant_liste),
                CommandHandler('retour', start),
                CommandHandler('transport', bienvenueTransport)
            ],

            RESTAURANT_RESULTATS: [
                RegexHandler('^(Kebab House|Pizza Express|Kookeat|Tasty chicken spot|Punjabi)$',
                             restaurant_detail),
                CommandHandler('transport', bienvenueTransport),
                CommandHandler('retour', resto_type_liste)
            ],

            RESTAURANT_DETAIL: [
                CommandHandler('retour', restaurant_liste),
                CommandHandler('transport', bienvenueTransport)
            ],

            SORTIE_CHOIX: [
                RegexHandler('^(Musée)$', musee_recommendation),
                RegexHandler('^(Bar)$', bar_recommendation),
                RegexHandler('^(Club)$', club_recommendation),
                RegexHandler('^(Restaurant)$', resto_type_liste),
                CommandHandler('transport', bienvenueTransport),
                CommandHandler('retour', start)
            ],

            SORTIE_RECOMMENDATIONS: [
                CommandHandler('retour', sortie_type_liste),
                CommandHandler('transport', bienvenueTransport)
            ],

            TRANSPORT: [
                CommandHandler('start', start),
                MessageHandler(Filters.text, lieu_a_chercher),
                MessageHandler(Filters.location, coordonnees_a_traiter),
                CommandHandler('cancel', cancel),
                MessageHandler(Filters.command, details_arret)
            ],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
