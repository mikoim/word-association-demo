import moment from "moment";
import "moment/locale/ja";

export function getMomentInstance(
  epoch: number | string,
  millis = false
): moment.Moment {
  let n = 0;

  if (typeof epoch == "string") {
    n = parseInt(epoch);
  } else {
    n = epoch;
  }

  if (!millis) {
    n *= 1000;
  }

  return moment(n);
}

export function getMomentNow(): moment.Moment {
  return moment();
}

export function getMomentInstanceByString(
  datetime: string | undefined
): moment.Moment {
  return moment(datetime);
}

export function getJstTimestamp(
  epoch: number | string,
  millis = false
): string {
  if (!epoch) return "";
  return getMomentInstance(epoch, millis).format("YYYY年M月D日(ddd) HH:mm:ss");
}
