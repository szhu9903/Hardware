

const colorArr = ["magenta", "red", "volcano", "orange", "gold", "lime", "green", "cyan", "blue", "geekblue"]

export function getColorArr() {
  let index = Math.floor(Math.random()*10);
  return colorArr[index];
}

export const blogPageSize = 10;
export const sysPageSize = 12;

// export const baseWs = 'ws://127.0.0.1:8890/hardware/ws'
export const baseWs = 'wss://hardware.zsjblog.com/hardware/ws'

