from database.distributore_DAO import DistributoreDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # TODO
        result = []
        for distrubutore in self._distributori:
            prezzi = distrubutore.get_prezzi()
            prezzo_mese = [p.prezzo_litro for p in prezzi if p.data.month == mese]

            media = 0
            if prezzo_mese: #è True solo se la lista non è vuota
                media = sum(prezzo_mese)/len(prezzo_mese)
            result.append((distrubutore.nome, media))
        return result

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if len(sequenza_parziale) == 7:
            if costo_corrente < self.__costo_ottimo or self.__costo_ottimo == -1:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = sequenza_parziale[:]
            return

        for distr_id in prezzi_settimana.keys():
            costo = prezzi_settimana[distr_id][giorno -1] * 100
            if ultimo_distributore is not None and distr_id != ultimo_distributore:
                costo += 5
            sequenza_parziale.append(distr_id)
            self.__ricorsione(sequenza_parziale, giorno + 1, distr_id, costo_corrente + costo, prezzi_settimana)
            sequenza_parziale.pop()

    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        # TODO
        prezzi_settimana = {}
        for distributore in self._distributori:
            prezzi = distributore.get_prezzi()

            prezzi_mese = [p for p in prezzi if p.data.month == mese]
            prezzi_mese.sort(key=lambda p: p.data)
            prezzi_settimana[distributore.id] = [p.prezzo_litro for p in prezzi_mese[:7]]
        return prezzi_settimana