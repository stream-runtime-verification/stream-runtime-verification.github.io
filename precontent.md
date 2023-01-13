---
title: Stream Runtime Verification
lastupdate: January 2023
---

# Table of contents
(@about) [About](#about)
(@onlineoffline) [Online vs. offline monitoring](#onlinevsoffline)
(@synchasynch) [Synchronous vs. asynchronous SRV](#synchasynch)
(@features) [Language features](#features)
(@projects) [Projects](#projects)
(@bibliography) [Bibliography](#bibliography)

## @about. About {#about}
%
% What is RV
%
Runtime verification (RV) is a dynamic technique for software quality
assurance that consists of generating a monitor from a formal
specification.
%
At runtime, the monitor inspects traces of the execution of the system
under analysis, detecting violations of the specification.

![SRV architecture](assets/images/srv.svg){ width=600px }

%
% Languages for RV
%
Motivated by the counterparts in static verification, early RV
specification languages were based on temporal
logics \cite{havelund02synthesizing,eisner03reasoning,bauer11runtime},
regular expressions \cite{sen03generating}, timed regular
expressions \cite{TRE}, rules \cite{barringer04rule}, or
rewriting \cite{rosu05rewriting}.
%
% SRV
%
Stream runtime verification (SRV), pioneered by
Lola \citesrv{dangelo05lola}, defines monitors declaratively by
equations that define the dependencies between output streams of
results and input streams of observations, where the types of the
streams and operations can be rich types of data.
%
Unlike logical techniques, that compute Boolean verdicts, SRV allows
rich observations and verdicts.
%
Examples include counting events, specifying and computing robustness
values, generating models, quantitative verdicts and calculating
target spatial coordinates.
%
See \citesrv{dangelo05lola,faymonville16stream,gorostiaga21striver, danielsson19decentralized} for examples illustrating the
expressivity of SRV languages.
%
The keystone of SRV is to separate two concerns: the temporal
dependencies and the data manipulated.
%
The temporal dependencies are inspired by the algorithms to monitor
temporal logics which essentially capture the order of operations in
monitoring algorithms.
%
The data manipulation describes how to perform each individual
operation and each element of storage that the monitor handles.
%
The data stored and computed is modeled as data types (data theories
in the jargon of SRV) whose implementation is independent of the model
of time.
%
Most system include a handful of wired data
types (e.g. \citesrv{dangelo05lola,faymonville19streamlab,convent18tessla})
but others study how to transparently incorporate data-types from
programming languages \citesrv{ceresa20declarative}.

### Runtime verification vs. static verification.
Static verification techniques like model checking intend to show that
every (infinite) run of a system satisfies a given specification,
while runtime verification is concerned only with a single (finite)
trace.
%
Thus, RV sacrifices completeness to provide an applicable formal
extension of testing.
%
See \cite{leucker09brief,havelund05verify} for modern surveys on
runtime verification and the recent book \cite{bartocci18lectures}.

## @onlineoffline. Online vs. offline monitoring {#onlinevsoffline}
There are two kinds of monitoring algorithms in RV depending on when
the trace is generated and processed.
%
In online monitoring the monitor checks the trace while the system
runs, while in offline monitoring a finite collection of previously
generated traces are analyzed.
%
Online monitoring is used to detect violations of the specification
when the system is in operation, while offline monitoring is used in
post-mortem analysis and for testing large systems before deployment.

% Efficiency of online/offline of past/future specs
%
The online monitoring problem of past specifications can be solved
efficiently using constant space and linear time in the trace size.
%
For future properties, on the other hand, the space requirement
depends on the length of the trace for rich types (even though for
LTL, that is for the verdict domain of the Booleans, one can use
automata techniques to reduce the necessary space to exponential in
the size of the specification).
%
Consequently, online monitoring of future temporal formulas quickly
becomes intractable in practical applications with long traces.
%
On the other hand, the offline monitoring problem for LTL-like logics
is known to be easy for purely past or purely future properties.
%
% Efficiently monitoriable/trace length independence
%
We detail in the paper a syntactic characterization of
*efficiently monitorable* specifications (introduced
in \citesrv{dangelo05lola}), for which the space requirement of the
online monitoring algorithm is independent of the size of the trace,
and linear in the specification size.
%
This property was later popularized as *trace length
independence* \citesrv{bauer13from} and is a very desirable property as
it allows online monitors to scale to arbitrarily large traces.
%
In practice, most properties of interest in online monitoring can be
expressed as efficiently monitorable properties.
%
For the offline monitoring problem, there is an efficient monitoring
strategy in the presence of arbitrary past and future combinations by
scheduling trace length independent passes.
%
An execution of the monitor extracted from a Lola specification
computes data values at each position by evaluating the expressions
over streams of input, incrementally computing the output streams.

## @synchasynch. Synchronous vs. asynchronous SRV {#synchasynch}
Different temporal algorithms exist for different notions of time.
%
Early SRV works consider streams to be synchronized sequences of data
(like in LTL semantics), so data observed in different streams at the
same index in their sequences are considered to have occurred at the
same time.
%
Examples of synchronous SRV formalisms include the original
Lola \citesrv{dangelo05lola} and systems like
Copilot \citesrv{pike10copilot}.
%
Other formalisms that can be easily described using SRV include
Mission-time LTL \cite{reinbacher14temporal} and Functional Reactive
Programming (FRP) \cite{eliot97functional}.
%
Synchronous languages, like Lustre \cite{halbwachs91synchronous},
Esterel \cite{berry00foundations} and Signal \cite{gautier87signal}
also define relations between input and output values but these are
designed to express behaviors so they assume causality and forbid
future references, while in SRV future references are allowed to
describe monitors that depend on future observations.


%
There have been approaches to extend SRV to real-time event streams,
including RTLola \citesrv{faymonville17realtime},
TeSSLa \citesrv{convent18tessla} and Striver \citesrv{gorostiaga21striver},
which consider streams to be sequences of timed events.
%
Events contain data and are time-stamped with the instant of time at
which the data is produced (either observed or generated).
%
The time stamps of a stream must be monotonically increasing, but the
events at a given index in two different streams can have arbitrary
time stamps.
%
These formalisms are known as asynchronous or real-time SRV.
%
See \citesrv{gorostiaga20unifying} for a expressiveness comparison
between synchronous time and asynchronous SRV.

![Synchronous vs. asynchronous streams](assets/images/synchasynch.svg){ width=600px }

## @features. Language features {#features}

### Static parameterization
Static parametrization is a feature of some SRV systems which allows
defining an abstract specification and instantiate it with concrete
values later on.
%
This is useful to reuse repetitive specifications and capture the
essence of a stream definition, abstracting away the irrelevant
specific values
%
This feature is implemented in Lola2.0 \citesrv{faymonville16stream} as
well as in TeSSLa \citesrv{convent18tessla} using an ad-hoc macro feature
in the tool chain; and in HLola \citesrv{ceresa20declarative} and HStriver
\citesrv{gorostiaga21hstriver} as functions in the host language.

### Dynamic parameterization
Some tools like Lola2.0 \citesrv{faymonville16stream} offer the
possibility of instantiating a parameterized stream with values that
are discovered in the middle of a trace.

## @projects. Projects {#projects}
### SRV and Temporal Task Planning
Temporal task planning guarantees a robot will succeed in its task
as long as certain explicit and implicit assumptions about the
robot's operating environment, sensors, and capabilities hold.
A robot executing a plan can *silently fail* to fulfill the task if the
assumptions are violated at runtime.
Monitoring assumption violations at runtime  can flag silent failures and also
provide mitigation and remediation opportunities. However, this requires means
for describing assumptions combining temporal and quantitative data, automatic
construction of correct monitors and ensuring a correct interplay between the
planning execution and monitors.

In this project \cite{zudaire21assumption} we propose combining temporal
planning with stream runtime verification, which offers a high-level language
to describe monitors together with guarantees on execution time and memory
usage. 
% 
We demonstrate our approach both in real and simulated flights for
some typical mission scenarios. 

<div class="i-frame">
  <iframe
    width="560"
    height="315"
    src="https://www.youtube.com/embed/3lVxiFWCYE4"
    title="YouTube video player"
    frameborder="10"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  ></iframe>

## @bibliography. Bibliography {#bibliography}
### SRV Bibliography
\thebibliographysrv

### Other Bibliography
\thebibliography
