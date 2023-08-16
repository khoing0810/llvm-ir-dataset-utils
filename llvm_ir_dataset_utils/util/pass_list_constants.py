# This module contains a list of pass constants that are used throughout the
# project while doing various analyses.

LOOP_PASS_LIST = [
    'IndVarSimplifyPass',
    'LICMPass',
    'LoopDeletionPass',
    'LoopDistributionPass',
    'LoopFullUnrollPass',
    'LoopIdiomRecognizePass',
    'LoopInstSimplifyPass',
    'LoopLoadEliminationPass',
    'LoopRotatePass',
    'LoopSimplifyCFGPass',
    'LoopSimplifyPass',
    'LoopSinkPass',
    'LoopUnrollPass',
    'LoopVectorizePass',
    'SimpleLoopUnswitchPass',
]

OPT_DEFAULT_O3_PASS_LIST = [
    'Annotation2MetadataPass1', 'ForceFunctionAttrsPass1',
    'InferFunctionAttrsPass1', 'CoroEarlyPass1', 'LowerExpectIntrinsicPass1',
    'SimplifyCFGPass1', 'SROAPass1', 'EarlyCSEPass1', 'CallSiteSplittingPass1',
    'OpenMPOptPass1', 'IPSCCPPass1', 'CalledValuePropagationPass1',
    'GlobalOptPass1', 'PromotePass1', 'InstCombinePass1', 'SimplifyCFGPass2',
    'RequireAnalysisPass<llvm::GlobalsAA, llvm::Module>1',
    'InvalidateAnalysisPass<llvm::AAManager>1',
    'RequireAnalysisPass<llvm::ProfileSummaryAnalysis, llvm::Module>1',
    'InlinerPass1', 'InlinerPass2', 'PostOrderFunctionAttrsPass1',
    'ArgumentPromotionPass1', 'OpenMPOptCGSCCPass1', 'SROAPass2',
    'EarlyCSEPass2', 'SpeculativeExecutionPass1', 'JumpThreadingPass1',
    'CorrelatedValuePropagationPass1', 'SimplifyCFGPass3', 'InstCombinePass2',
    'AggressiveInstCombinePass1', 'LibCallsShrinkWrapPass1',
    'TailCallElimPass1', 'SimplifyCFGPass4', 'ReassociatePass1',
    'RequireAnalysisPass<llvm::OptimizationRemarkEmitterAnalysis, llvm::Function>1',
    'LoopSimplifyPass1', 'LCSSAPass1', 'LoopInstSimplifyPass1',
    'LoopSimplifyCFGPass1', 'LICMPass1', 'LoopRotatePass1',
    'SimpleLoopUnswitchPass1', 'SimplifyCFGPass5', 'InstCombinePass3',
    'LCSSAPass2', 'LoopIdiomRecognizePass1', 'IndVarSimplifyPass1',
    'LoopDeletionPass1', 'LoopFullUnrollPass1', 'SROAPass3',
    'VectorCombinePass1', 'MergedLoadStoreMotionPass1', 'GVNPass1', 'SCCPPass1',
    'BDCEPass1', 'InstCombinePass4', 'JumpThreadingPass2',
    'CorrelatedValuePropagationPass2', 'ADCEPass1', 'MemCpyOptPass1',
    'DSEPass1', 'LCSSAPass3', 'CoroElidePass1', 'SimplifyCFGPass6',
    'InstCombinePass5', 'CoroSplitPass1', 'InlinerPass3', 'InlinerPass4',
    'PostOrderFunctionAttrsPass2', 'ArgumentPromotionPass2',
    'OpenMPOptCGSCCPass2', 'CoroSplitPass2',
    'InvalidateAnalysisPass<llvm::ShouldNotRunFunctionPassesAnalysis>1',
    'DeadArgumentEliminationPass1', 'CoroCleanupPass1', 'GlobalOptPass2',
    'GlobalDCEPass1', 'EliminateAvailableExternallyPass1',
    'ReversePostOrderFunctionAttrsPass1', 'RecomputeGlobalsAAPass1',
    'Float2IntPass1', 'LowerConstantIntrinsicsPass1', 'LCSSAPass4',
    'LoopDistributePass1', 'InjectTLIMappings1', 'LoopVectorizePass1',
    'LoopLoadEliminationPass1', 'InstCombinePass6', 'SimplifyCFGPass7',
    'SLPVectorizerPass1', 'VectorCombinePass2', 'InstCombinePass7',
    'LoopUnrollPass1', 'WarnMissedTransformationsPass1', 'SROAPass4',
    'InstCombinePass8',
    'RequireAnalysisPass<llvm::OptimizationRemarkEmitterAnalysis, llvm::Function>2',
    'LCSSAPass5', 'AlignmentFromAssumptionsPass1', 'LoopSinkPass1',
    'InstSimplifyPass1', 'DivRemPairsPass1', 'TailCallElimPass2',
    'SimplifyCFGPass8', 'GlobalDCEPass2', 'ConstantMergePass1',
    'CGProfilePass1', 'RelLookupTableConverterPass1', 'AnnotationRemarksPass1',
    'VerifierPass1', 'BitcodeWriterPass1'
]