#include "xbrz.h"
#include "filter.h"

#ifdef _WIN32
#define SRWW_EXPORT __declspec(dllexport)
#else
#define SRWW_EXPORT __attribute__((visibility("default")))
#endif

// Thin entry points into the repository's unmodified DeSmuME xBRZ 1.4.
// RGB is the same mode used by DeSmuME's Render4xBRZ display filter.
extern "C" SRWW_EXPORT
void srww_xbrz4_rgb(const uint32_t* src, uint32_t* dst, int w, int h) {
    SSurface input = {}, output = {};
    input.Surface = reinterpret_cast<unsigned char*>(const_cast<uint32_t*>(src));
    input.Width = w; input.Height = h; input.Pitch = w * 4;
    output.Surface = reinterpret_cast<unsigned char*>(dst);
    output.Width = w * 4; output.Height = h * 4; output.Pitch = w * 16;
    Render4xBRZ(input, output);
}

// Alpha-aware variant for producing transparent artwork reference files.
extern "C" SRWW_EXPORT
void srww_xbrz4_argb(const uint32_t* src, uint32_t* dst, int w, int h) {
    xbrz::scale<4, xbrz::ColorFormatARGB>(src, dst, w, h);
}
