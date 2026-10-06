import Mathlib.Combinatorics.SimpleGraph.Coloring.FiniteReachability
import Mathlib.Combinatorics.SimpleGraph.Coloring.FiveColorExtension
import Mathlib.Combinatorics.SimpleGraph.Coloring.Kempe
import Mathlib.Combinatorics.SimpleGraph.Coloring.KempeBoundary
import Mathlib.Combinatorics.SimpleGraph.Coloring.KempeMass
import Mathlib.Combinatorics.SimpleGraph.Coloring.KempeRepartition
import Mathlib.Combinatorics.SimpleGraph.PlaneMap
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.BeltOpeningWords
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.BreadcrumbWarning
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.Construction
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.DegreeFiveOutside
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.DeleteVertex
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.ErasePermutation
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.Examples
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FaceChord
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FaceCorner
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiniteFourExtension
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColor
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorDemo
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorExamples
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorSeparation
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorTheorem
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FourColorExtension
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FourColorSmallOrder
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FourEliminationOrder
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.Icosahedron
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.InsertPermutation
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.Jordan
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanCycle
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanEven
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanFace
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanGrow
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanSides
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanSplit
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanTwoSides
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanWalkParity
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationBoundary
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationBridgeFills
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationDelete
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationInsert
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationSplit
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationSplitFills
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationSystem
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SharedHub
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SingletonExterior
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalChordInsert
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalCompletion
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalDegree
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalDelete
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalFiveColor
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalFourContact
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalMap
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalMassContact
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalRankedContact
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalSmallOrder
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SupportTransport
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleBasic
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleChain
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleCut
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleDegen
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleFlip
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleMoves
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleNoSingleton
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleRules
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBelt
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltAllRoots
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltCaps
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltTransport
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltWalk
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyCliqueLift
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyLemmaL4
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyMobility
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyMobilityGeneral
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyMobilityTriangulated
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyPotential
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyProtectedLift
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyShortFill
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancySlide
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyThreeMoveObstruction
open Lean Elab Command

/-- Studio sweep: every non-internal constant declared in the snapshot Mathlib modules. -/
def auditMods : List Name := [
  `Mathlib.Combinatorics.SimpleGraph.Coloring.FiniteReachability,
  `Mathlib.Combinatorics.SimpleGraph.Coloring.FiveColorExtension,
  `Mathlib.Combinatorics.SimpleGraph.Coloring.Kempe,
  `Mathlib.Combinatorics.SimpleGraph.Coloring.KempeBoundary,
  `Mathlib.Combinatorics.SimpleGraph.Coloring.KempeMass,
  `Mathlib.Combinatorics.SimpleGraph.Coloring.KempeRepartition,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.BeltOpeningWords,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.BreadcrumbWarning,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.Construction,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.DegreeFiveOutside,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.DeleteVertex,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.ErasePermutation,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.Examples,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.FaceChord,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.FaceCorner,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiniteFourExtension,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColor,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorDemo,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorExamples,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorSeparation,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorTheorem,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.FourColorExtension,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.FourColorSmallOrder,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.FourEliminationOrder,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.Icosahedron,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.InsertPermutation,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.Jordan,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanCycle,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanEven,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanFace,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanGrow,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanSides,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanSplit,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanTwoSides,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanWalkParity,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationBoundary,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationBridgeFills,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationDelete,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationInsert,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationSplit,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationSplitFills,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationSystem,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SharedHub,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SingletonExterior,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalChordInsert,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalCompletion,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalDegree,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalDelete,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalFiveColor,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalFourContact,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalMap,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalMassContact,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalRankedContact,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalSmallOrder,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.SupportTransport,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleBasic,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleChain,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleCut,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleDegen,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleFlip,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleMoves,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleNoSingleton,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleRules,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBelt,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltAllRoots,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltCaps,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltTransport,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltWalk,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyCliqueLift,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyLemmaL4,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyMobility,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyMobilityGeneral,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyMobilityTriangulated,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyPotential,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyProtectedLift,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyShortFill,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancySlide,
  `Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyThreeMoveObstruction]

#eval show CommandElabM Unit from do
  let env ← getEnv
  let idxs := auditMods.filterMap env.getModuleIdx?
  let mut n : Nat := 0
  let mut bad : Array (Name × Name) := #[]
  for (c, _) in env.constants.toList do
    if let some i := env.getModuleIdxFor? c then
      if idxs.contains i && !c.isInternal then
        n := n + 1
        let axs ← liftCoreM (collectAxioms c)
        for a in axs do
          if a != ``propext && a != ``Classical.choice && a != ``Quot.sound then
            bad := bad.push (c, a)
  logInfo m!"modules found: {idxs.length} of {auditMods.length}; constants checked: {n}; nonstandard: {bad.size}; {bad.toList.take 20}"

#print axioms SimpleGraph.SphericalMap.five_color_theorem
#print axioms SimpleGraph.PlaneMap.five_color_theorem
#print axioms SimpleGraph.PlaneMap.exists_five_colouring
#print axioms SimpleGraph.VacancyLemmaL4.l4a
#print axioms SimpleGraph.VacancyLemmaL4.l4b
#print axioms SimpleGraph.TheoremPPole.theoremP
#print axioms SimpleGraph.TheoremPPole.theoremP_fill_or_singleton
