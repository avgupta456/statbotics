import { FaGithub } from "react-icons/fa";
import { RxMoon, RxSun } from "react-icons/rx";

import type { AppProps } from "next/app";
import Image from "next/image";
import Link from "next/link";

import {
  ActionIcon,
  AppShell,
  Burger,
  MantineProvider,
  createTheme,
  useComputedColorScheme,
  useMantineColorScheme,
} from "@mantine/core";
import "@mantine/core/styles.css";
import { useDisclosure } from "@mantine/hooks";

import "../styles/globals.css";
import { loaderProp } from "../utils/utils";

const theme = createTheme({
  fontFamily: "Roboto, sans-serif",
  cursorType: "pointer",
});

function Navbar({ opened, toggle }: { opened: boolean; toggle: () => void }) {
  // -> colorScheme is 'auto' | 'light' | 'dark'
  const { colorScheme, setColorScheme } = useMantineColorScheme();
  // -> computedColorScheme is 'light' | 'dark', argument is the default value
  const computedColorScheme = useComputedColorScheme("light");

  const toggleColorScheme = () => {
    setColorScheme(computedColorScheme === "dark" ? "light" : "dark");
  };

  const sunIcon = <RxSun className="h-5 w-5 text-yellow-500" stroke={4} />;
  const moonIcon = <RxMoon className="h-5 w-5 text-blue-600" stroke={2.5} />;

  return (
    <AppShell.Header>
      <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
      <div className="m-3 flex items-center">
        <div className="flex">
          <Link href="/" className="mr-8 flex items-center gap-2 text-xl font-thin">
            <Image
              src="/circ_favicon.ico"
              alt="logo"
              width={30}
              height={30}
              loader={loaderProp}
              unoptimized
            />
            Statbotics
          </Link>
        </div>

        <div className="flex-grow" />
        <ActionIcon
          component={Link}
          href="https://github.com/avgupta456/statbotics"
          target="_blank"
          rel="noopener noreferrer"
          variant="subtle"
          color={colorScheme === "dark" ? "gray" : "black"}
          className="mr-2"
          radius="md"
        >
          <FaGithub className="h-5 w-5" stroke={2} />
        </ActionIcon>
        <ActionIcon variant="subtle" color="gray" onClick={toggleColorScheme} radius="md">
          {colorScheme === "dark" ? sunIcon : moonIcon}
        </ActionIcon>
      </div>
    </AppShell.Header>
  );
}

export default function App({ Component, pageProps }: AppProps) {
  const [opened, { toggle }] = useDisclosure();

  return (
    <MantineProvider theme={theme}>
      <AppShell
        header={{ height: 55 }}
        navbar={{
          width: 300,
          breakpoint: "sm",
          collapsed: { mobile: !opened },
        }}
        padding="md"
      >
        <Navbar opened={opened} toggle={toggle} />
        <AppShell.Main>
          <Component {...pageProps} />
        </AppShell.Main>
      </AppShell>
    </MantineProvider>
  );
}
