import satori from "satori";
import { Resvg } from "@resvg/resvg-js";
import type { APIRoute } from "astro";

const FONT_URL =
  "https://fonts.gstatic.com/s/bricolagegrotesque/v9/3y9U6as8bTXq_nANBjzKo3IeZx8z6up5BeSl5jBNz_19PpbpMXuECpwUxJBOm_OJWiaaD30YfKfjZZoLvZvlyM0.ttf";

export const GET: APIRoute = async () => {
  const fontData = await fetch(FONT_URL).then((r) => r.arrayBuffer());

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
          // Logo mark
          {
            type: "div",
            props: {
              style: {
                width: 48,
                height: 48,
                borderRadius: "50%",
                border: "3px solid #ff5c28",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              },
              children: [
                {
                  type: "div",
                  props: {
                    style: {
                      width: 14,
                      height: 14,
                      borderRadius: "50%",
                      background: "#ff5c28",
                    },
                  },
                },
              ],
            },
          },
          // Headline
          {
            type: "div",
            props: {
              style: {
                fontSize: 84,
                fontWeight: 800,
                color: "#1a1d22",
                lineHeight: 1.05,
                maxWidth: 900,
              },
              children: "Build Outcome\nMachines.",
            },
          },
          // Tagline + URL row
          {
            type: "div",
            props: {
              style: {
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-end",
              },
              children: [
                {
                  type: "div",
                  props: {
                    style: {
                      fontSize: 28,
                      color: "rgba(26,29,34,0.60)",
                      maxWidth: 660,
                      lineHeight: 1.4,
                    },
                    children:
                      "AI systems that own an outcome — and improve it continuously.",
                  },
                },
                {
                  type: "div",
                  props: {
                    style: {
                      fontSize: 20,
                      color: "#ff5c28",
                      fontWeight: 800,
                      letterSpacing: "0.02em",
                    },
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
        {
          name: "Bricolage Grotesque",
          data: fontData,
          weight: 800,
          style: "normal",
        },
      ],
    }
  );

  const png = new Resvg(svg).render().asPng();
  return new Response(png, {
    headers: { "Content-Type": "image/png", "Cache-Control": "public, max-age=31536000, immutable" },
  });
};
