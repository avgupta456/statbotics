// Needed to declare this as a module. Also shows that imports
// function normally in workers.
const ctx: Worker = self as unknown as Worker;

async function start() {
  // sleep for 5 seconds
  await new Promise((resolve) => setTimeout(resolve, 5000));
  ctx.postMessage({
    type: "tsData",
    data: "Testing123ABC",
  });
}

ctx.addEventListener("message", (evt) => {
  switch (evt.data.type) {
    case "start":
      start();
      return;
  }
});

export {};
