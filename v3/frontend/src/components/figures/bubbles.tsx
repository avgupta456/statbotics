import React, { useCallback, useEffect, useMemo, useState } from "react";
import { IoMdEye } from "react-icons/io";

import { Button, Tooltip } from "@mantine/core";
import { Annotation, CircleSubject, Label } from "@visx/annotation";
import { Axis, Orientation } from "@visx/axis";
import { RectClipPath } from "@visx/clip-path";
import { localPoint } from "@visx/event";
import { Group } from "@visx/group";
import { withParentSize } from "@visx/responsive";
import { scaleLinear } from "@visx/scale";
import { Circle, LinePath } from "@visx/shape";
import { TooltipWithBounds, withTooltip } from "@visx/tooltip";
import { WithTooltipProvidedProps } from "@visx/tooltip/lib/enhancers/withTooltip";
import { voronoi } from "@visx/voronoi";
import { Zoom } from "@visx/zoom";

import { useLocation } from "../../contexts/locationContext";
import { usePreferences } from "../../contexts/preferencesContext";
import { DISTRICT_FULL_NAMES, STATE_FULL_NAMES } from "../../utils/geography";
import LocationFilter from "../location";
import Select from "../select";

const initialTransform = {
  scaleX: 1,
  scaleY: 1,
  translateX: 0,
  translateY: 0,
  skewX: 0,
  skewY: 0,
};

const sharedTickLabelProps = { fontSize: 12, fontFamily: "sans-serif" } as const;
const xTickLabelProps = { ...sharedTickLabelProps, textAnchor: "middle" } as const;
const yTickLabelProps = { ...sharedTickLabelProps, textAnchor: "end" } as const;

const sharedLabelProps = { fontSize: 13, fontFamily: "sans-serif" } as const;
const xLabelProps = { ...sharedLabelProps, y: 40 } as const;
const yLabelProps = { ...sharedLabelProps, y: -30 } as const;

type Datum = {
  label: string;
  x: number;
  y: number;
  z?: number;
};

type DotsProps = {
  width: number;
  height: number;
  data: Datum[];
  selectedTeam: string | null;
};

let tooltipTimeout: number;

const RawBubbles = withTooltip<DotsProps, Datum>(
  ({
    width,
    height,
    data,
    selectedTeam,
    hideTooltip,
    showTooltip,
    tooltipOpen,
    tooltipData,
    tooltipLeft,
    tooltipTop,
  }: DotsProps & WithTooltipProvidedProps<Datum>) => {
    const { colorScheme } = usePreferences();

    const textColor = colorScheme === "dark" ? "#fff" : "#000";

    const dataXMin = Math.min(...data.map((d) => d.x));
    const dataXMax = Math.max(...data.map((d) => d.x));
    const dataYMin = Math.min(...data.map((d) => d.y));
    const dataYMax = Math.max(...data.map((d) => d.y));
    const dataZMin = Math.min(...data.map((d) => d.z ?? 0));
    const dataZMax = Math.max(...data.map((d) => d.z ?? 1));
    const dataXRange = dataXMax - dataXMin;
    const dataYRange = dataYMax - dataYMin;

    const buffer = 0.1;
    const xMin = dataXMin - buffer * dataXRange;
    const xMax = dataXMax + buffer * dataXRange;
    const yMin = dataYMin - buffer * dataYRange;
    const yMax = dataYMax + buffer * dataYRange;

    const xScale = useMemo(
      () => scaleLinear<number>({ domain: [xMin, xMax], range: [0, width] }),
      [width],
    );
    const yScale = useMemo(
      () => scaleLinear<number>({ domain: [yMin, yMax], range: [height, 0] }),
      [height],
    );

    const voronoiLayout = useMemo(
      () =>
        voronoi<Datum>({
          x: (d) => xScale(d.x) ?? 0,
          y: (d) => yScale(d.y) ?? 0,
          width,
          height,
        })(data),
      [width, height, xScale, yScale, data],
    );

    // event handlers
    const handleMouseMove = useCallback(
      (zoom: any, event: React.MouseEvent | React.TouchEvent) => {
        if (tooltipTimeout) clearTimeout(tooltipTimeout);
        if (!zoom?.containerRef?.current) return;

        const { scaleX, scaleY, translateX, translateY } = zoom.transformMatrix;

        // find the nearest polygon to the current mouse position
        const point = localPoint(zoom?.containerRef?.current, event);
        if (!point) return;
        const neighborRadius = 100;
        const closest = voronoiLayout.find(
          (point.x - translateX) / scaleX,
          (point.y - translateY) / scaleY,
          neighborRadius,
        );
        if (closest) {
          showTooltip({
            tooltipLeft: xScale(closest.data.x) * scaleX + translateX,
            tooltipTop: yScale(closest.data.y) * scaleY + translateY,
            tooltipData: closest.data,
          });
        }
      },
      [xScale, yScale, showTooltip, voronoiLayout],
    );

    const handleMouseLeave = useCallback(() => {
      tooltipTimeout = window.setTimeout(() => {
        hideTooltip();
      }, 300);
    }, [hideTooltip]);

    const [teamsToLabel, setTeamsToLabel] = useState<number[]>([]);

    useEffect(() => {
      const teamToIndex = new Map<string, number>();
      for (let i = 0; i < data.length; i += 1) {
        teamToIndex.set(data[i].label, i);
      }

      setTeamsToLabel(
        [
          ...data.sort((a, b) => b.x - a.x).slice(0, 10),
          ...data.sort((a, b) => b.y - a.y).slice(0, 10),
          ...data.sort((a, b) => b.x + b.y - a.x - a.y).slice(0, 20),
        ]
          .map((point) => teamToIndex.get(point.label) ?? 0)
          .filter((value, index, self) => self.indexOf(value) === index),
      );
    }, [data]);

    const findTeamIndex = data.findIndex((d) => d.label === selectedTeam);

    const cutoffs = Array.from(Array(21).keys()).map(
      (i) => xMin + yMin + (dataXRange + dataYRange) * ((i - 5) / 10),
    );

    return (
      <Zoom<SVGSVGElement>
        width={width}
        height={height}
        scaleXMin={1}
        scaleXMax={100}
        scaleYMin={1}
        scaleYMax={100}
        initialTransformMatrix={initialTransform}
      >
        {(zoom) => {
          const { scaleX, scaleY, translateX, translateY } = zoom.transformMatrix;
          const zoomXMin = xScale.invert(-translateX / scaleX);
          const zoomXMax = xScale.invert((width - translateX) / scaleX);
          const zoomYMin = yScale.invert((height - translateY) / scaleY);
          const zoomYMax = yScale.invert(-translateY / scaleY);

          return (
            <div className="relative">
              <svg
                width={width}
                height={height}
                style={{ cursor: zoom.isDragging ? "grabbing" : "grab", touchAction: "none" }}
                ref={zoom.containerRef}
              >
                <RectClipPath id="zoom-clip" width={width} height={height} />
                {/** capture all mouse events with a rect */}
                <rect
                  width={width}
                  height={height}
                  rx={14}
                  fill={colorScheme === "dark" ? "#30404d" : "#fff"}
                  onMouseMove={(event) => handleMouseMove(zoom, event)}
                  onMouseLeave={handleMouseLeave}
                  onTouchMove={(event) => handleMouseMove(zoom, event)}
                  onTouchEnd={handleMouseLeave}
                />
                {cutoffs.map((cutoff) => (
                  <LinePath
                    stroke={colorScheme === "light" ? "#ddd" : "#555"}
                    strokeWidth={1}
                    data={[
                      { x: cutoff - 2 * yMax, y: 2 * yMax },
                      { x: 2 * xMax, y: cutoff - 2 * xMax },
                    ]}
                    x={(d) => xScale(d.x) * scaleX + translateX}
                    y={(d) => yScale(d.y) * scaleY + translateY}
                  />
                ))}
                <g transform={zoom.toString()}>
                  <Group pointerEvents="none">
                    {data.map((point) => {
                      const z = point?.z ?? 1;
                      const radius =
                        (5 * (z - dataZMin)) / (dataZMax - dataZMin) / zoom.transformMatrix.scaleX;
                      return (
                        <Circle
                          key={`point-${point.label}`}
                          className="dot"
                          cx={xScale(point.x)}
                          cy={yScale(point.y)}
                          r={radius}
                          fill={tooltipData?.label === point.label ? "#f87171" : "#3884ff"}
                        />
                      );
                    })}
                  </Group>
                </g>
                {data?.length > Math.max(...teamsToLabel) &&
                  teamsToLabel.map((index) => (
                    <Label
                      x={xScale(data[index].x) * scaleX + translateX}
                      y={yScale(data[index].y) * scaleY + translateY}
                      showAnchorLine={false}
                      showBackground={false}
                      title={data[index].label}
                      fontColor={textColor}
                      titleFontSize={10}
                      verticalAnchor="start"
                      horizontalAnchor="middle"
                    />
                  ))}
                {data?.length > findTeamIndex && findTeamIndex >= 0 && (
                  <Annotation
                    x={xScale(data[findTeamIndex].x) * scaleX + translateX}
                    y={yScale(data[findTeamIndex].y) * scaleY + translateY}
                  >
                    <CircleSubject
                      radius={10}
                      fill="transparent"
                      stroke="#f87171"
                      strokeWidth={3}
                    />
                  </Annotation>
                )}
                <Axis
                  orientation={Orientation.bottom}
                  top={height - 45}
                  scale={scaleLinear({
                    domain: [zoomXMin, zoomXMax],
                    range: [0, width],
                  })}
                  stroke={textColor}
                  tickStroke={textColor}
                  tickLabelProps={{ ...xTickLabelProps, fill: textColor }}
                  label="Total Points"
                  labelProps={{ ...xLabelProps, fill: textColor }}
                />
                <Axis
                  orientation={Orientation.left}
                  left={45}
                  scale={scaleLinear({
                    domain: [zoomYMin, zoomYMax],
                    range: [height, 0],
                  })}
                  stroke={textColor}
                  tickStroke={textColor}
                  tickLabelProps={{ ...yTickLabelProps, fill: textColor }}
                  label="Endgame Points"
                  labelProps={{ ...yLabelProps, fill: textColor }}
                />
              </svg>
              {!(scaleX === 1 && translateX === 0 && translateY === 0) && (
                <div className="absolute right-2 top-2">
                  <Button onClick={zoom.reset} variant="filled" size="xs">
                    Reset Focus
                  </Button>
                </div>
              )}
              {tooltipOpen && tooltipData && tooltipLeft != null && tooltipTop != null && (
                <TooltipWithBounds left={tooltipLeft + 10} top={tooltipTop + 10}>
                  <div className="text-xs text-gray-900">
                    <strong>Team {tooltipData.label}</strong>
                    <br className="h-1" />({tooltipData.x.toFixed(2)}, {tooltipData.y.toFixed(2)})
                  </div>
                </TooltipWithBounds>
              )}
            </div>
          );
        }}
      </Zoom>
    );
  },
);

function Bubbles({
  data,
  showLocationQuickFilter = true,
}: {
  data: any[];
  showLocationQuickFilter?: boolean;
}) {
  const { location, setLocation } = useLocation();

  const [selectedTeam, setSelectedTeam] = useState<string | null>(null);

  const getX = (d: any) => d?.epa?.breakdown?.teleop_points?.mean ?? 0;
  const getY = (d: any) => d?.epa?.breakdown?.auto_points?.mean ?? 0;
  const getZ = (d: any) => d?.epa?.breakdown?.endgame_points?.mean ?? 0;

  const finalData = useMemo(() => {
    const filterData = (d: any) => {
      if (!location) return true;
      const prefix = location.split("_")[0];
      const suffix = location.split("_")[1];
      if (prefix === "country") {
        return d?.country === suffix;
      }
      if (prefix === "state") {
        return STATE_FULL_NAMES[d?.state] === suffix;
      }
      if (prefix === "district") {
        return DISTRICT_FULL_NAMES[d?.district] === suffix;
      }
      return false;
    };

    const setAxes = (d: any) => {
      const name = d?.name;
      const label = d?.team;
      const x = getX(d);
      const y = getY(d);
      const z = getZ(d);
      return { name, label, x, y, z };
    };

    return data.filter(filterData).map(setAxes);
  }, [data, location]);

  const ResponsiveBubbles = withParentSize(({ parentWidth, parentHeight }) => (
    <RawBubbles
      width={parentWidth ?? 0}
      height={parentHeight ?? 0}
      data={finalData}
      selectedTeam={selectedTeam}
    />
  ));

  return (
    <div>
      <div className="mx-2 mt-4 flex w-full flex-row justify-center">
        <div className="flex items-center gap-4">
          <Tooltip label="Clear filters">
            <div className="cursor-pointer">
              <IoMdEye
                className="h-6 w-6 text-gray-600"
                onClick={() => {
                  setLocation(null);
                }}
              />
            </div>
          </Tooltip>
          {showLocationQuickFilter && <LocationFilter />}
          <Select
            data={finalData.map((d: any) => ({ value: d.label, label: `${d.label} | ${d.name}` }))}
            value={selectedTeam}
            onChange={setSelectedTeam}
            limit={20}
            placeholder="Find a team"
            searchable
            clearable
          />
        </div>
      </div>
      <div className="mt-8 h-[500px] px-8">
        <ResponsiveBubbles />
      </div>
    </div>
  );
}

export default Bubbles;
