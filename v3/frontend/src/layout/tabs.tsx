import { Tabs } from "@mantine/core";

export default function TabPanel({
  value,
  children,
  loading = false,
  error = false,
  ...props
}: {
  value: string;
  children: any;
  loading?: boolean;
  error?: boolean;
  props?: any;
}) {
  // TODO: Add loading and error states

  if (loading) {
    return (
      <Tabs.Panel value={value} {...props}>
        <div>Loading...</div>
      </Tabs.Panel>
    );
  }

  if (error) {
    return (
      <Tabs.Panel value={value} {...props}>
        <div>Error</div>
      </Tabs.Panel>
    );
  }

  return (
    <Tabs.Panel value={value} {...props}>
      {children}
    </Tabs.Panel>
  );
}
