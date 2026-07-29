---
layout: default
title: Query Sequences
parent: Dataset
nav_order: 2
---

# Query sequences

Five representative scenes are used to query against the reference data. As mapping sensors, we employed four different camera systems to acquire query images with different characteristics, including resolution, field of view, and camera models. The four camera systems are: a Canon EOS R equipped with a 24 mm or 35 mm lens, a GoPro Hero 7, and an iPhone 14 Pro (Table 1).

<style>
.camera-table {
  border-collapse: collapse;
}
.camera-table th, .camera-table td {
  text-align: center;
  border: 0.25px solid #ccc;
}
.camera-table .total-row td {
  font-weight: bold;
}
</style>

<table class="camera-table">
  <thead>
    <tr>
      <th rowspan="2">Camera</th>
      <th colspan="2" class="fov-h">FoV [°]</th>
      <th rowspan="2">Camera model</th>
      <th rowspan="2">Resolution</th>
    </tr>
    <tr>
      <th class="fov-h">h</th>
      <th>v</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Canon 24mm</td><td class="fov-h">72.3</td><td>51.9</td><td>Pinhole</td><td>6720 × 4480</td></tr>
    <tr><td>Canon 35mm</td><td class="fov-h">53.3</td><td>37.0</td><td>Pinhole</td><td>6720 × 4480</td></tr>
    <tr><td>GoPro Hero 7</td><td class="fov-h">122.6</td><td>94.4</td><td>Fisheye</td><td>4000 × 3000</td></tr>
    <tr><td>iPhone 14 Pro</td><td class="fov-h">57.1</td><td>71.9</td><td>Pinhole</td><td>1440 × 1920</td></tr>
  </tbody>
</table>
***Table 1:*** *Cameras used for query sequence acquisition.*

The query image acquisition was conducted in late winter (February) 2025 under predominantly overcast conditions, resulting in mainly diffuse illumination. At that time, the trees were free of foliage. In each scene, a sequence of images was captured with all four cameras. The sequences differ in trigger rate, trajectory, length, and number of images (Table 2), since each camera was operated independently, one after another, using its own capture method. The Canon camera was triggered manually, ensuring the images were captured in roughly an upright orientation. For the GoPro, an upright configuration was also targeted. Instead of manual triggering, a video was recorded at 24 frames per second (FPS). For iPhone 14 Pro sequences, Pix4DCatch was used and image triggering was set according to distance and angle criteria of 0.1 m and 15°, respectively. During this capture, the iPhone was deliberately pointed slightly towards the ground and, at times, moved rapidly to create a trajectory similar to walking while using an AR navigation application. For each sequence, we tried to create a single or multiple closed loops.

## Image counts

<div style="overflow-x: auto;">
<table class="camera-table">
  <thead>
    <tr>
      <th>Camera</th>
      <th>Scene 1</th>
      <th>Scene 2</th>
      <th>Scene 3</th>
      <th>Scene 4</th>
      <th>Scene 5</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Canon 24mm</td><td>165</td><td>194</td><td>135</td><td>142</td><td>165</td><td>801</td></tr>
    <tr><td>Canon 35mm</td><td>154</td><td>158</td><td>116</td><td>168</td><td>181</td><td>777</td></tr>
    <tr><td>GoPro Hero 7</td><td>415</td><td>376</td><td>370</td><td>383</td><td>403</td><td>1947</td></tr>
    <tr><td>iPhone 14 Pro</td><td>435</td><td>246</td><td>350</td><td>380</td><td>463</td><td>1874</td></tr>
    <tr class="total-row"><td>Total</td><td>1169</td><td>974</td><td>971</td><td>1073</td><td>1212</td><td>5399</td></tr>
  </tbody>
</table>
</div>
***Table 2:*** *Number of images acquired per scene and camera.*

## Calibration

The query cameras (Canon EOS R, GoPro Hero 7, iPhone 14 Pro) are self-calibrated: their calibration parameters are estimated jointly with the image poses during the bundle adjustment (see [Ground-Truth Generation](#ground-truth-generation) below). Using the estimated parameters, all query images are undistorted to follow a standard camera model: pinhole for the Canon EOS R and iPhone, and equidistant fisheye for the GoPro

## Ground-truth generation

Query images are co-registered to the reference imagery using a multi-stage SfM-based procedure in Agisoft Metashape. Since each scene contains four sequences with many overlapping images, no direct query-to-reference image correspondences are needed — a stable photogrammetric model of the query sequences is built first, then co-registered to the reference data using manually measured corresponding points.
- **Building the photogrammetric model**: the four sequences per scene are first aligned individually, using at least three control points (CPs) per sequence to bring them into a unified global reference frame; a second alignment pass then uses these poses to efficiently find matches across sequences. All CPs, plus ~30 additional distinctive tie points per scene, are measured in ~15 images from different camera sequences to mutually stabilize them
- **Co-registering to the reference data**: ~20–25 clearly identifiable points per scene are manually measured in the reference images (drawn from the CPs and tie points), with 3D coordinates estimated by triangulation from the fixed reference poses. At least three of these points per scene are held out from the bundle adjustment as independent check points
  - Points used for co-registration: relative ground control points (RGCPs)
  - Held-out check points: relative control points (RCPs)
- A final bundle adjustment jointly optimizes the query image poses and camera calibration parameters, with RGCPs introduced at a 3D standard deviation of 0.005 m (see [Calibration](#calibration) above for how these parameters are then applied)

**Co-registration accuracy** per scene (RMSE of RGCP residuals / RCP position differences) is reported in Table 3, confirming sub-centimeter co-registration accuracy across all scenes.

<table class="camera-table">
  <thead>
    <tr>
      <th>Scene</th>
      <th>RGCP # pts</th>
      <th>RGCP 3D RMSE [m]</th>
      <th>RCP # pts</th>
      <th>RCP 3D RMSE [m]</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Scene 1</td><td>17</td><td>0.007</td><td>3</td><td>0.007</td></tr>
    <tr><td>Scene 2</td><td>19</td><td>0.008</td><td>4</td><td>0.006</td></tr>
    <tr><td>Scene 3</td><td>20</td><td>0.006</td><td>6</td><td>0.006</td></tr>
    <tr><td>Scene 4</td><td>17</td><td>0.006</td><td>3</td><td>0.004</td></tr>
    <tr><td>Scene 5</td><td>16</td><td>0.005</td><td>4</td><td>0.003</td></tr>
  </tbody>
</table>
***Table 3:*** *Co-registration accuracy per scene, based on RGCP residuals and held-out RCP position differences.*

**Georeferencing accuracy** per scene (RMSE between RTK-GNSS check-point positions and the corresponding coordinates from the final estimated image poses) is reported in Table 4, confirming a lower-centimeter range and validating the co-registration.

<table class="camera-table">
  <thead>
    <tr>
      <th>Scene</th>
      <th># Points</th>
      <th>3D RMSE [m]</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Scene 1</td><td>11</td><td>0.014</td></tr>
    <tr><td>Scene 2</td><td>10</td><td>0.025</td></tr>
    <tr><td>Scene 3</td><td>7</td><td>0.030</td></tr>
    <tr><td>Scene 4</td><td>9</td><td>0.021</td></tr>
    <tr><td>Scene 5</td><td>11</td><td>0.019</td></tr>
  </tbody>
</table>
***Table 4:*** *Absolute georeferencing accuracy per scene.*

## Scene 1

**Characteristics**: A local access road in a suburban environment, with sidewalks on both sides of the street and a pedestrian crossing with a small island. The street traverses a residential neighborhood of detached houses and abundant greenery, including hedges and trees.

<img src="/assets/gifs/scene_1.gif" alt="Scene 1 preview" style="display: block; width: 60%; margin: 0 auto;">

## Scene 2

**Characteristics**: A local access road in an area characterized by multi-story commercial, industrial, and office buildings. Road construction is ongoing on the street and in its immediate surroundings; as a result, no road markings are visible and numerous temporary construction fences are in place. On both sides of the road, there are wide sidewalks and some unfinished flower beds without plants.

<img src="/assets/gifs/scene_2.gif" alt="Scene 2 preview" style="display: block; width: 60%; margin: 0 auto;">

## Scene 3

**Characteristics**: A busy, multi-lane main road in a commercial environment, featuring car dealers and a fuel station, with many dynamic objects, such as cars. On both sides of the street, there is a sidewalk and only a small amount of vegetation.

<img src="/assets/gifs/scene_3.gif" alt="Scene 3 preview" style="display: block; width: 60%; margin: 0 auto;">

## Scene 4

**Characteristics**: A local access road with an integrated cycle path, traversing a neighborhood with multi-story urban residential and commercial buildings. Sidewalks are provided on both sides of the street, separated by flower beds. The environment is densely vegetated, with trees and hedges.

<img src="/assets/gifs/scene_4.gif" alt="Scene 4 preview" style="display: block; width: 60%; margin: 0 auto;">

## Scene 5

**Characteristics**: A narrow residential street in a neighborhood of detached houses, with plenty of greenery, including large trees and hedges. Various cars are parked on the side of the road.

<img src="/assets/gifs/scene_5.gif" alt="Scene 5 preview" style="display: block; width: 60%; margin: 0 auto;">
