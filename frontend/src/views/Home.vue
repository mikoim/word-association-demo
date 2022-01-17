<template>
  <v-container>
    <v-row justify="center">
      <v-col xl="4" lg="5" md="6">
        <v-card>
          <v-card-title>
            {{ targetWord }}
          </v-card-title>
          <v-card-text>
            <v-img
              :src="imageUrl"
              :lazy-src="imageUrl"
              aspect-ratio="1"
              class="grey lighten-2"
            >
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular
                    indeterminate
                    color="grey lighten-5"
                  ></v-progress-circular>
                </v-row>
              </template>
            </v-img>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col xl="4" lg="5" md="6">
        <v-card>
          <v-card-text>
            <v-progress-linear
              class="mb-6"
              color="light-blue"
              height="10"
              :value="step > 0 ? (score / step) * 100 : 0"
              striped
            ></v-progress-linear>
            <v-text-field
              v-model="inputWord"
              autofocus
              outlined
              clearable
              label="連想される単語"
              hint="連想される日本語の単語を入力"
              :disabled="loading"
              @keydown.enter="processWord"
            ></v-text-field>
            <v-btn
              block
              x-large
              color="primary"
              @click="processWord"
              :loading="loading"
              >確認</v-btn
            >
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col xl="4" lg="5" md="6">
        <v-card>
          <v-card-title>履歴</v-card-title>
          <v-card-text>
            <template>
              <v-simple-table>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left">目標単語</th>
                      <th class="text-left">入力単語</th>
                      <th class="text-left">コサイン類似度</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in histories" :key="item.step">
                      <td>{{ item.target }}</td>
                      <td>{{ item.input }}</td>
                      <td>{{ item.cosineSimilarity }}</td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </template>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar
      v-model="snackbar.enabled"
      :timeout="snackbar.timeout"
      :color="snackbar.color"
    >
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar.enabled = false">
          閉じる
        </v-btn></template
      ></v-snackbar
    >
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import moment from "moment";

import { DefaultApi } from "@/client";
import { clientFactory } from "@/Api";

interface Snackbar {
  enabled: boolean;
  text: string;
  color: string;
  timeout: number;
}

interface History {
  step: number;
  target: string;
  input: string;
  cosineSimilarity: number;
}

interface Data {
  api: DefaultApi;
  snackbar: Snackbar;
  loading: boolean;

  histories: History[];

  inputWord: string;
  targetWord: string;
  imageUrl: string;

  score: number;
  step: number;
}

moment.locale("ja");

export default Vue.extend({
  name: "Home",
  metaInfo: {
    title: "連想ゲーム",
  },

  components: {},

  data: (): Data => ({
    api: clientFactory(),
    snackbar: {
      enabled: false,
      text: "",
      color: "",
      timeout: 3000,
    },
    loading: false,
    histories: [],
    inputWord: "",
    targetWord: "",
    imageUrl: "",
    score: 0,
    step: 0,
  }),

  async mounted() {
    await this.processWord();
  },

  methods: {
    // snackbar
    openSnackbar(text: string, color: string) {
      this.snackbar = {
        enabled: true,
        text: text,
        color: color,
        timeout: 3000,
      };
    },
    infoSnackbar(text: string) {
      this.openSnackbar(text, "primary");
    },
    successSnackbar(text: string) {
      this.openSnackbar(text, "success");
    },
    errorSnackbar(text: string) {
      this.openSnackbar(text, "error");
    },

    // eslint-disable-next-line
    handleException(e: any) {
      if (e.response) {
        this.errorSnackbar(e.response.data);
      } else {
        this.errorSnackbar(e);
      }
    },

    async processWord() {
      const choice = (array: string[]) => {
        return array[Math.floor(Math.random() * array.length)];
      };

      const getDistance = async (a: string, b: string) => {
        let res = (await this.api.predictWordsDistanceGet(a, b)).data;
        return res.cosine_similarity;
      };

      const getRelatedWord = async (a: string) => {
        let words = (await this.api.predictWordsWordsGet(a)).data.words;

        for (const word of words) {
          const w = word.word;
          if (w !== this.inputWord && w !== this.targetWord) {
            return w;
          }
        }

        return words.slice(-1)[0].word;
      };

      const getImage = async (a: string) => {
        let urls = (await this.api.searchImageImagesGet(a)).data.urls;
        return choice(urls);
      };

      if (this.targetWord === this.inputWord && this.inputWord !== "") {
        this.errorSnackbar("異なる単語を入力してください");
        return;
      } else if (this.inputWord.length === 0 && this.step > 0) {
        this.errorSnackbar("単語を入力してください");
        return;
      }

      this.loading = true;

      if (this.targetWord === "") {
        try {
          this.targetWord = await getRelatedWord("家族");
          this.imageUrl = await getImage(this.targetWord);
        } catch (e) {
          this.handleException(e);
        }
      } else {
        try {
          const score = await getDistance(this.targetWord, this.inputWord);
          this.score += score;
          this.histories.push({
            step: this.step,
            target: this.targetWord,
            input: this.inputWord,
            cosineSimilarity: score,
          });

          const previousTarget = this.targetWord;
          const previousInput = this.inputWord;

          this.targetWord = await getRelatedWord(this.inputWord);
          this.inputWord = "";
          this.imageUrl = await getImage(this.targetWord);

          if (score > 0.5) {
            this.successSnackbar(
              `${previousTarget} 対 ${previousInput} = ${score}`
            );
          } else {
            this.errorSnackbar(
              `${previousTarget} 対 ${previousInput} = ${score}`
            );
          }

          this.step += 1;
        } catch (e) {
          this.handleException(e);
        }
      }

      this.loading = false;
    },
  },
});
</script>
