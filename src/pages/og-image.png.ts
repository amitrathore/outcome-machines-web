import satori from "satori";
import { Resvg } from "@resvg/resvg-js";
import type { APIRoute } from "astro";

const FONT_BRICOLAGE =
  "https://fonts.gstatic.com/s/bricolagegrotesque/v9/3y9U6as8bTXq_nANBjzKo3IeZx8z6up5BeSl5jBNz_19PpbpMXuECpwUxJBOm_OJWiaaD30YfKfjZZoLvZvlyM0.ttf";
const FONT_NOTO =
  "https://fonts.gstatic.com/s/notosans/v42/o-0mIpQlx3QUlC5A4PNB6Ryti20_6n1iPHjcz6L1SoM-jCpoiyD9A99d.ttf";

export const GET: APIRoute = async () => {
  const [fontData, notoData] = await Promise.all([
    fetch(FONT_BRICOLAGE).then((r) => r.arrayBuffer()),
    fetch(FONT_NOTO).then((r) => r.arrayBuffer()),
  ]);

  const svg = await satori(
    {
      type: "div",
      props: {
        style: {
          width: "100%",
          height: "100%",
          background: "#f5f1e9",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: "72px 80px",
          fontFamily: "Bricolage Grotesque",
        },
        children: [
          // Top: word + pronunciation
          {
            type: "div",
            props: {
              style: { display: "flex", alignItems: "baseline", gap: 28 },
              children: [
                {
                  type: "div",
                  props: {
                    style: { fontSize: 62, fontWeight: 800, color: "#1a1d22" },
                    children: "outcome machine",
                  },
                },
                {
                  type: "div",
                  props: {
                    style: { fontSize: 24, fontWeight: 400, color: "rgba(26,29,34,0.40)", fontFamily: "Noto Sans" },
                    children: "/ˈaʊtkʌm məˈʃiːn/",
                  },
                },
              ],
            },
          },
          // Ruled line
          {
            type: "div",
            props: {
              style: {
                height: 1,
                background: "rgba(26,29,34,0.15)",
                width: "100%",
              },
            },
          },
          // Middle: noun + definition + example
          {
            type: "div",
            props: {
              style: { display: "flex", flexDirection: "column", gap: 18 },
              children: [
                {
                  type: "div",
                  props: {
                    style: { fontSize: 22, fontWeight: 800, color: "#ff5c28", letterSpacing: "0.08em" },
                    children: "NOUN",
                  },
                },
                {
                  type: "div",
                  props: {
                    style: {
                      fontSize: 30,
                      fontWeight: 800,
                      color: "rgba(26,29,34,0.78)",
                      lineHeight: 1.5,
                      maxWidth: 980,
                    },
                    children:
                      "An AI system purpose-built to own a single business outcome — that monitors, explains, recommends, executes, and learns until the number moves.",
                  },
                },
                {
                  type: "div",
                  props: {
                    style: {
                      fontSize: 22,
                      fontWeight: 800,
                      color: "rgba(26,29,34,0.42)",
                      lineHeight: 1.5,
                      maxWidth: 860,
                    },
                    children:
                      '"We deployed an Outcome Machine for revenue recovery. It paid for itself in six weeks."',
                  },
                },
              ],
            },
          },
          // Bottom: logo mark + domain
          {
            type: "div",
            props: {
              style: { display: "flex", justifyContent: "space-between", alignItems: "center" },
              children: [
                // Circle logo mark
                {
                  type: "div",
                  props: {
                    style: {
                      width: 40,
                      height: 40,
                      borderRadius: "50%",
                      border: "2.5px solid #ff5c28",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    },
                    children: [
                      {
                        type: "div",
                        props: {
                          style: { width: 12, height: 12, borderRadius: "50%", background: "#ff5c28" },
                        },
                      },
                    ],
                  },
                },
                // Domain
                {
                  type: "div",
                  props: {
                    style: { fontSize: 18, fontWeight: 800, color: "#ff5c28", letterSpacing: "0.03em" },
                    children: "outcomemachines.com",
                  },
                },
              ],
            },
          },
        ],
      },
    },
    {
      width: 1200,
      height: 630,
      fonts: [
        { name: "Bricolage Grotesque", data: fontData, weight: 800, style: "normal" },
        { name: "Noto Sans", data: notoData, weight: 400, style: "normal" },
      ],
    }
  );

  const png = new Resvg(svg).render().asPng();
  return new Response(png, {
    headers: { "Content-Type": "image/png", "Cache-Control": "public, max-age=31536000, immutable" },
  });
};
