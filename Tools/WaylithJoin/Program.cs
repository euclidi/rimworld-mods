using System;
using System.IO;
using Waylith.Graphics.Textures;

if (args.Length != 2) throw new ArgumentException("Usage: WaylithJoin input.split output.dds");
if (!DdsFile.TryJoin(File.ReadAllBytes(args[0]), out var data, out var length))
    throw new InvalidDataException("The installed Waylith could not join this split DDS.");
File.WriteAllBytes(args[1], data.AsSpan(0, length).ToArray());
