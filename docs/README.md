# OeD: Open-ended Dependency Analyser

OeD looks at open-ended dependencies (OeD): dependencies that multiple
package versions can satisify. For instance, 'green>=3.1' is
open-ended since any version above or equals to 3.1 should work.

We explore here whether these OeD actually work, or these are just a
pipe dream. We look in particular to Python packages, but in principle
the idea applies to other programming languages such as
Java,Javascript, Ruby, and the likes that uses some form of OeD.
